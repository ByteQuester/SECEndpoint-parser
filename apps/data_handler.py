"""
This class manages data operations.
"""
import os
import pandas as pd

from apps.configs import SnowflakeConfig
from apps.functions import SECAPIClient, SnowflakeDataManager, LoggingManager, DataStorageManager, AnnualDataProcessor, QuarterlyDataProcessor
from apps.queries import ASSET_LIABILITIES, CASH_FLOW, DEBT_MANAGEMENT, LIQUIDITY, MARKET_VALUATION, OPERATIONAL_EFFICIENCY, PROFITABILITY, QUERY_FILES
from apps.utils import FileVersionManager


class DataPipelineIntegration:
    def __init__(self, cik_number=None, use_snowflake=True, snowflake_config=None, local_storage_dir='data'):
        self.cik_number = cik_number
        self.use_snowflake = use_snowflake
        self.local_storage_dir = local_storage_dir
        self.sec_client = SECAPIClient()
        if self.use_snowflake:
            self.snowflake_config = snowflake_config if snowflake_config else SnowflakeConfig()
            self.snowflake_manager = SnowflakeDataManager(self.snowflake_config)
        self.error_handler = LoggingManager()
        self.document = FileVersionManager(base_dir=local_storage_dir)
        self.data_storage_manager = DataStorageManager(local_storage_dir, cik_number)
        self._init_metrics()

    def _init_metrics(self):
        self.metrics = {
            'Annual': ['CapitalExpendituresIncurredButNotYetPaid', 'NetCashProvidedByUsedInOperatingActivities',
                       'NetCashProvidedByUsedInInvestingActivities', 'NetCashProvidedByUsedInFinancingActivities'],
            'Quarterly': ['Assets', 'Liabilities', 'StockholdersEquity', 'AssetsCurrent', 'LiabilitiesCurrent',
                          'OperatingIncomeLoss', 'Revenues', 'NetIncomeLoss']
        }
        self.category_metric_map = {
            # 'Investment Efficiency': ['CapitalExpendituresIncurredButNotYetPaid', 'NetIncomeLoss', 'Assets'],
            'Liquidity': ['AssetsCurrent', 'LiabilitiesCurrent'],
            # 'Assets and Liabilities': ['Assets', 'Liabilities', 'StockholdersEquity'],
            'Profitability': ['OperatingIncomeLoss', 'Revenues', 'NetIncomeLoss']
            # 'Cash Flow': ['NetCashProvidedByUsedInOperatingActivities', 'NetCashProvidedByUsedInInvestingActivities', 'NetCashProvidedByUsedInFinancingActivities']
        }

    def fetch_data(self, cik_number=None):
        """
        Fetch data from the SEC API using the given CIK number.
        """
        cik = cik_number if cik_number else self.cik_number
        if not cik:
            self.error_handler.log("CIK number is not provided.", "ERROR")
            return {"error": "CIK number is required"}

        try:
            company_facts = self.sec_client.fetch_company_facts(cik)
            if 'error' in company_facts:
                self.error_handler.log(f"Error fetching data for CIK {cik}: {company_facts['error']}", "ERROR")
                return company_facts
            return company_facts
        except Exception as e:
            self.error_handler.log_error(e, "ERROR")
            return {"error": str(e)}

    def preprocess_data(self, raw_data):
        """
        Preprocess the raw data using the defined metrics, store using FileVersionManager, and store the data.
        Args:
            raw_data (dict): The raw data fetched from the SEC API.
        """
        try:
            df = pd.DataFrame(raw_data)
            annual_processor = AnnualDataProcessor(df)
            quarterly_processor = QuarterlyDataProcessor(df)

            for category, metrics in self.category_metric_map.items():
                if category in ['Assets and Liabilities', 'Liquidity', 'Profitability']:
                    preprocessed_data = quarterly_processor.process_data(metrics)
                else:
                    preprocessed_data = annual_processor.process_data(metrics)

                if self.use_snowflake:
                    self.snowflake_manager.upload_data(preprocessed_data, category)
                    self.error_handler.log(f"Preprocessed data for {category} uploaded to Snowflake.", "INFO")
                else:
                    file_name = self.data_storage_manager.store_data(preprocessed_data, 'preprocessed_data', category)
                    if file_name:
                        self.document.update_index(self.cik_number, category, file_name, 'preprocessed_data')
                    else:
                        self.error_handler.log(f"Failed to store preprocessed data for {category}", "ERROR")

        except Exception as e:
            self.error_handler.log_error(e, "ERROR")
            return {"error": str(e)}

    def process_and_store_data(self, specific_queries=None):
        """
        Process the preprocessed data by running queries and store the results.
        Args:
            specific_queries (list of str, optional): Specific queries to execute. If None, all categories are processed.
        """
        try:
            categories_to_process = specific_queries if specific_queries else self.category_metric_map.keys()

            for category in categories_to_process:
                # Check if the category is valid
                if category not in self.category_metric_map:
                    self.error_handler.log(f"Invalid category or query name: {category}", "WARNING")
                    continue

                # Retrieve the preprocessed data file path for the category
                preprocessed_file_path = self.data_storage_manager.get_processed_data_file_path(category)
                if not preprocessed_file_path:
                    self.error_handler.log(f"No preprocessed data found for {category}", "WARNING")
                    continue

                # Execute the query related to the category
                query_result = self.execute_query(category)

                # Store the query result if it's valid
                if query_result and category in query_result and query_result[category] is not None:
                    processed_file_name = self.data_storage_manager.store_data(query_result[category], 'processed_data',
                                                                               category)

                    # Update index file with the new or updated file path
                    if processed_file_name:
                        self.document.update_index(self.cik_number, category, processed_file_name, 'processed_data')

                else:
                    self.error_handler.log(f"No valid results for query {category}.", "WARNING")

        except Exception as e:
            self.error_handler.log_error(e, "ERROR")
            return {"error": str(e)}

    def execute_query(self, query_names):
        """
        Execute one or more SQL queries based on their names.
        Args:
            query_names (str or list of str): Name(s) of the query(ies) to execute.
        Returns:
            dict: A dictionary with query names as keys and query results as values.
        """
        if isinstance(query_names, str):
            query_names = [query_names]

        results = {}
        for query_name in query_names:
            query_filename = QUERY_FILES.get(query_name)
            if query_filename is None:
                self.error_handler.log(f"Query name '{query_name}' not found.", "ERROR")
                results[query_name] = None
                continue

            if self.use_snowflake:
                results[query_name] = self.snowflake_manager.execute_query_from_file(query_filename)
            else:
                results[query_name] = self._execute_query_locally(query_name)

        return results

    def _execute_query_locally(self, query_name):
        """
        Execute a query on locally stored data using a query file.
        Args:
            query_name (str): Path to a SQL file containing the query.
        Returns:
            DataFrame: Query results as a pandas DataFrame.
        """
        # Adjust the file path to match the new storage structure
        processed_file_path = self.data_storage_manager.get_processed_data_file_path(query_name)
        if not os.path.exists(processed_file_path):
            self.error_handler.log(f"No processed data file found for query {query_name}.", "ERROR")
            return None
        df = pd.read_csv(processed_file_path)

        if query_name == 'Assets Liabilities':
            return ASSET_LIABILITIES(df)
        elif query_name == 'Cash Flow':
            return CASH_FLOW(df)
        elif query_name == 'Debt Management':
            return DEBT_MANAGEMENT(df)
        elif query_name == 'Liquidity':
            return LIQUIDITY(df)
        elif query_name == 'Operational Efficiency':
            return OPERATIONAL_EFFICIENCY(df)
        elif query_name == 'Market Valuation':
            return MARKET_VALUATION(df, stock_price_df=None)  # TODO: implement stock price
        elif query_name == 'Profitability':
            return PROFITABILITY(df)
        else:
            self.error_handler.log(f"Query name '{query_name}' not implemented for local execution.", "ERROR")
