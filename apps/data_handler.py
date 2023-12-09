"""
This class manages data operations.
"""
import os
import pandas as pd
from pandasql import sqldf

from apps.configs import SnowflakeConfig
from apps.functions import SECAPIClient, FinancialDataProcessor, SnowflakeDataManager, LoggingManager
from apps.queries import QUERY_FILES, ASSET_LIABILITIES, CASH_FLOW, DEBT_MANAGEMENT, LIQUIDITY, MARKET_VALUATION , OPERATIONAL_EFFICIENCY


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

    def _setup_local_storage(self):
        """
        Set up the local storage directory.
        """
        if not os.path.exists(self.local_storage_dir):
            os.makedirs(self.local_storage_dir)
            self.error_handler.log(f"Created local storage directory at {self.local_storage_dir}", "INFO")

    def store_data_locally(self, data, file_name=None):
        """
        Store data in a CSV file locally.
        """
        if file_name is None:
            file_name = f"data_{self.cik_number}.csv" if self.cik_number else "data.csv"
        file_path = os.path.join(self.local_storage_dir, file_name)

        try:
            data.to_csv(file_path, index=False)
            self.error_handler.log(f"Data stored locally at {file_path}", "INFO")
        except Exception as e:
            self.error_handler.log_error(e, "ERROR")

    def store_data(self, data):
        """
        Store the processed data either locally or in Snowflake.
        """
        if self.use_snowflake:
            self.snowflake_manager.upload_data(data)
        else:
            self.store_data_locally(data, file_name=None)

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

    def execute_query(self, query_name):
        """
        Execute a SQL query based on its name.
        Args:
            query_name (str): Name of the query to execute.
        Returns:
            DataFrame: Query results as a pandas DataFrame.
        """
        query_filename = QUERY_FILES.get(query_name)
        if query_filename is None:
            self.error_handler.log(f"Query name '{query_name}' not found.", "ERROR")
            return None

        if self.use_snowflake:
            return self.snowflake_manager.execute_query_from_file(query_filename)
        else:
            return self._execute_query_locally(query_filename)

    def _execute_query_locally(self, query_name):
        """
        Execute a query on locally stored data using a query file.
        Args:
            query_filename (str): Path to a SQL file containing the query.
        Returns:
            DataFrame: Query results as a pandas DataFrame.
        """
        data_file_path = os.path.join(self.local_storage_dir, f"data_{self.cik_number}.csv")
        df = pd.read_csv(data_file_path)

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
            return MARKET_VALUATION(df, stock_price_df=None)  # Replace None with stock_price_df if available
        else:
            self.error_handler.log(f"Query name '{query_name}' not implemented for local execution.", "ERROR")
            return None
