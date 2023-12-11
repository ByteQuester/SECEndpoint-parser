"""
This class manages data operations.
#TODO in execute query function implement a different a new name configuration: cik_query_YYYYMMDD.csv
"""
from datetime import datetime
import os
import pandas as pd

from apps.configs import SnowflakeConfig
from apps.functions import SECAPIClient, FinancialDataProcessor, SnowflakeDataManager, LoggingManager
from apps.queries import ASSET_LIABILITIES, CASH_FLOW, DEBT_MANAGEMENT, LIQUIDITY, MARKET_VALUATION , OPERATIONAL_EFFICIENCY, PROFITABILITY, QUERY_FILES
from apps.utils import FileVersionManager


class DataPipelineIntegration:
    def __init__(self, cik_number=None, use_snowflake=True, snowflake_config=None, local_storage_dir='data'):
        self.cik_number = cik_number
        self.use_snowflake = use_snowflake
        self.local_storage_dir = local_storage_dir
        self._setup_local_storage()
        self.sec_client = SECAPIClient()
        self.data_processor = FinancialDataProcessor(self.sec_client)
        if self.use_snowflake:
            self.snowflake_config = snowflake_config if snowflake_config else SnowflakeConfig()
            self.snowflake_manager = SnowflakeDataManager(self.snowflake_config)
        self.error_handler = LoggingManager()
        self.document = FileVersionManager()

    def _setup_local_storage(self):
        """
        Set up the local storage directory.
        """
        if not os.path.exists(self.local_storage_dir):
            os.makedirs(self.local_storage_dir)
            self.error_handler.log(f"Created local storage directory at {self.local_storage_dir}", "INFO")

    def store_data(self, data, query_name=None, timestamp=None):
        """
        Store the processed data either locally or in Snowflake.
        """
        if self.use_snowflake:
            self.snowflake_manager.upload_data(data)
        else:
            self.store_data_locally(data, query_name, timestamp)

    def store_data_locally(self, data, query_name=None, timestamp=None):
        """
        Store data in a CSV file locally.
        """
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y%m%d')
        if self.cik_number and query_name:
            cik_folder = str(int(self.cik_number))
            dir_path = os.path.join(self.local_storage_dir, cik_folder, query_name.replace(' ', '_'))
            os.makedirs(dir_path, exist_ok=True)
            file_name = f"{self.cik_number}_{query_name.replace(' ', '_')}_{timestamp}.csv"
            file_path = os.path.join(dir_path, file_name)
            try:
                data.to_csv(file_path, index=False)
                self.error_handler.log(f"Data stored locally at {file_path}", "INFO")
                self.document.update_index_file(self.cik_number, query_name, file_path)
            except Exception as e:
                self.error_handler.log_error(e, "ERROR")
        else:
            self.error_handler.log("CIK number or query name not provided.", "ERROR")

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

    def preprocess_data(self, data):
        """
        Preprocess the fetched data.
        """
        try:
            processed_data = self.data_processor.process_data({'company_facts': data})
            return processed_data
        except Exception as e:
            self.error_handler.log_error(e, "ERROR")
            return {"error": str(e)}

    def store_preprocessed_data(self, data):
        if self.cik_number:
            raw_dir_path = os.path.join(self.local_storage_dir, str(int(self.cik_number)), 'raw')
            os.makedirs(raw_dir_path, exist_ok=True)
            file_path = os.path.join(raw_dir_path, f"raw_data_{self.cik_number}.csv")
            data.to_csv(file_path, index=False)
            self.error_handler.log(f"Raw data stored locally at {file_path}", "INFO")
        else:
            self.error_handler.log("CIK number not provided.", "ERROR")

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
        raw_file_path = os.path.join(self.local_storage_dir, str(int(self.cik_number)), 'raw',
                                     f"raw_data_{self.cik_number}.csv")
        if not os.path.exists(raw_file_path):
            self.error_handler.log(f"No raw data file found for CIK {self.cik_number}.", "ERROR")
            return None
        df = pd.read_csv(raw_file_path)

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
            return MARKET_VALUATION(df, stock_price_df=None) #TODO: implement stock price
        elif query_name == 'Profitability':
            return PROFITABILITY(df)
        else:
            self.error_handler.log(f"Query name '{query_name}' not implemented for local execution.", "ERROR")
            return None
