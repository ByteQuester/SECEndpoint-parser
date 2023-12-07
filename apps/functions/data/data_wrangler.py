'''
This module provides a FinancialDataProcessor class for processing financial data.
The FinancialDataProcessor class handles the flattening and structuring of financial data
retrieved from the SEC API and converts it into a pandas DataFrame for further analysis.

Example usage:
    # Create an instance of FinancialDataProcessor
    processor = FinancialDataProcessor()

    # Process preprocessed data
    df = processor.process_data(preprocessed_data)

'''
import pandas as pd


class FinancialDataProcessor:
    def __init__(self, sec_api_client):
        """
        Initialize the FinancialDataProcessor with a SECAPIClient instance.

        Args:
            sec_api_client (SECAPIClient): An instance of the SECAPIClient class.
        """
        self.sec_api_client = sec_api_client

    def fetch_and_preprocess_data(self, cik_number):
        """
        Fetch and preprocess the financial data for a given CIK number.

        Args:
            cik_number (str): The CIK number of the company.

        Returns:
            dict: The preprocessed financial data.
        """
        company_facts = self.sec_api_client.fetch_company_facts(cik_number)
        if 'error' in company_facts:
            return {'error': company_facts['error']}

        submissions = self.sec_api_client.fetch_submissions(cik_number)
        if 'error' in submissions:
            return {'error': submissions['error']}

        # TODO: Implement specific preprocessing logic here

        return {'company_facts': company_facts, 'submissions': submissions}

    def process_data(self, preprocessed_data):
        """
        Flatten the preprocessed data into a tabular format.

        Args:
            preprocessed_data (dict): The preprocessed financial data.

        Returns:
            pd.DataFrame: The flattened data as a Pandas DataFrame.
        """
        flattened_data = []

        # Check if 'company_facts' is in the preprocessed data
        if 'company_facts' in preprocessed_data:
            entity = preprocessed_data['company_facts']
            entity_name = entity['EntityName']
            cik = entity['CIK']
            parsed_data = entity['ParsedData']

            for metric_key, metric_data in parsed_data.items():
                for item in metric_data:
                    end_date = item['end']
                    value = item['val']

                    flattened_data.append({
                        'EntityName': entity_name,
                        'CIK': cik,
                        'Metric': metric_key,
                        'End': end_date,
                        'Value': value
                    })
        # TODO: Implement flattening logic for other data types like submissions, tickers, etc.

        df = pd.DataFrame(flattened_data)
        return df

