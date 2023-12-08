"""
This class manages data operations.
"""
import os
import pandas as pd

from apps.configs import SnowflakeConfig
from apps.functions import SECAPIClient, FinancialDataProcessor, SnowflakeDataManager, LoggingManager


class DataPipelineIntegration:
    def __init__(self, cik_number=None, use_snowflake=True, snowflake_config=None, local_storage_dir='data'):
        # Store the CIK number
        self.cik_number = cik_number

        # Decide whether to use Snowflake for storage
        self.use_snowflake = use_snowflake

        # Local storage directory
        self.local_storage_dir = local_storage_dir

        self._setup_local_storage()
        # Initialize SEC API Client for fetching data
        self.sec_client = SECAPIClient()

        # Initialize Financial Data Processor for processing the data
        self.data_processor = FinancialDataProcessor(self.sec_client)

        if self.use_snowflake:
            # Use provided Snowflake configuration or default
            self.snowflake_config = snowflake_config if snowflake_config else SnowflakeConfig()
            self.snowflake_manager = SnowflakeDataManager(self.snowflake_config)

        # Initialize Logging Manager for logging activities
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
            # Storing data in Snowflake
            self.snowflake_manager.upload_data(data)
        else:
            # Storing data locally
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

    def execute_query(self, query, query_filename=None):
        """
        Execute a SQL query on the data.
        Args:
            query (str): SQL query string.
            query_filename (str): Path to a SQL file containing the query (optional).
        Returns:
            DataFrame: Query results as a pandas DataFrame.
        """
        if self.use_snowflake:
            # Execute query in Snowflake
            if query_filename:
                return self.snowflake_manager.execute_query_from_file(query_filename)
            else:
                return self.snowflake_manager.get_data(query)
        else:
            # Execute query on local data
            return self._execute_query_locally(query, query_filename)

    def _execute_query_locally(self, query, query_file_path=None):
        """
        Execute a query on locally stored data.
        Args:
            query (str): SQL query string.
            query_file_path (str): Path to a SQL file containing the query (optional).
        Returns:
            DataFrame: Query results as a pandas DataFrame.
        """
        # Read the local CSV file into a pandas DataFrame
        data_file_path = os.path.join(self.local_storage_dir, f"data_{self.cik_number}.csv")
        df = pd.read_csv(data_file_path)

        # If a query file path is provided, read the query from the file
        if query_file_path:
            with open(query_file_path, 'r') as file:
                query = file.read()

        # Execute the query using pandas querying capabilities
        return df.query(query)