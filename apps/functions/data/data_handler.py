"""
This class manages data operations.
"""


class SECDataHandler:
    def __init__(self, connect_to_snowflake=True, cik_number=None):
        """

        """
        self.connect_to_snowflake = connect_to_snowflake
        self.financial_data_processor = FinancialDataProcessor(SECAPIClient())
        self.snowflake_data_manager = SnowflakeDataManager()
        self.sec_api_client = SECAPIClient()
        self.cik_number = cik_number

    def retrieve_data(self, cik_number):
        """
        Retrieves data using the SECAPIClient.
        Returns:
            dict: The retrieved data.
        # TODO : make the CIK to be passed to this function dynamically
        """
        return self.sec_api_client.fetch_company_facts(cik_number)

    def process_data(self, data):
        """
        Processes the retrieved data using the FinancialDataProcessor.
        Args:
            data (dict): The retrieved data.
        Returns:
            dict: The processed data.
        """
        return self.financial_data_processor.process_data(data)

    def store_data(self, data):
        """
        Stores the processed data either in Snowflake using SnowflakeDataManager or locally.
        Args:
            data (dict): The processed data.
        """
        if self.connect_to_snowflake:
            self.snowflake_data_manager.upload_data(data)
        else:
            # Store data locally
            pass

    def retrieve_stored_data(self):
        """
        Retrieves the stored data either from Snowflake using SnowflakeDataManager or locally.
        Returns:
            dict: The retrieved data.
        """
        if self.connect_to_snowflake:
            return self.snowflake_data_manager.get_data()
        else:
            # Retrieve data locally
            pass
