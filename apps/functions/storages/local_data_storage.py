import os
import json
from apps.functions.managers import LoggingManager
from apps.utils import now


class DataStorageManager:
    def __init__(self, local_storage_dir, cik_number):
        self.local_storage_dir = local_storage_dir
        self.cik_number = cik_number
        self.error_handler = LoggingManager()
        self._setup_local_storage()

    def _setup_local_storage(self):
        if not os.path.exists(self.local_storage_dir):
            os.makedirs(self.local_storage_dir)
            self.error_handler.log(f"Created local storage directory at {self.local_storage_dir}", "INFO")

    def store_data(self, data, storage_type, category_name=None):
        timestamp = now()
        dir_path = self._get_dir_path(storage_type, category_name)
        file_name = f"{self.cik_number}_{category_name.replace(' ', '_') if category_name else 'data'}_{timestamp}"
        file_path = os.path.join(dir_path, f"{file_name}.csv")  # Adding .csv here
        if not os.path.exists(file_path):
            self._store_data_to_csv(data, dir_path, file_name)  # file_name without .csv
        return f"{file_name}.csv"

    def store_json_data(self, json_data, storage_type, category_name=None, sub_category=None):
        """
        Store JSON data in the designated directory for specific chart types.
        Args:
            json_data: Data to be stored
            storage_type: Type of storage (e.g., 'processed_json')
            category_name: Main category name (e.g., 'Profitability')
            sub_category: Sub-category or chart type (e.g., 'bar_chart')
        """
        timestamp = now()
        dir_path = self._get_extended_dir_path(storage_type, category_name, sub_category)
        file_name = f"{self.cik_number}_{category_name.replace(' ', '_') if category_name else 'data'}_{sub_category}_{timestamp}.json"
        file_path = os.path.join(dir_path, file_name)

        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        return file_name

    def _get_dir_path(self, storage_type, category_name):
        formatted_cik = f"{int(self.cik_number):010d}"
        dir_path = os.path.join(self.local_storage_dir, formatted_cik, storage_type,
                                category_name.replace(' ', '_') if category_name else '')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path

    def _get_extended_dir_path(self, storage_type, category_name, sub_category):
        """
        Create an extended directory path based on category and sub-category.
        """
        base_dir = os.path.join(self.local_storage_dir, str(self.cik_number), storage_type)
        if category_name:
            base_dir = os.path.join(base_dir, category_name.replace(' ', '_'))
        if sub_category:
            base_dir = os.path.join(base_dir, sub_category.replace(' ', '_'))

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        return base_dir

    def _store_data_to_csv(self, data, dir_path, file_name):
        file_path = os.path.join(dir_path, f"{file_name}.csv")
        try:
            data.to_csv(file_path, index=False)
            self.error_handler.log(f"Data stored locally at {file_path}", "INFO")
        except Exception as e:
            self.error_handler.log_error(e, "ERROR")

    def get_processed_data_file_path(self, query_name):
        """
        Get the path of the latest file for a specific query in processed_data.
        Args:
            query_name (str): The name of the query.
        Returns:
            str: The path of the latest file, or None if no file is found.
        """
        query_to_folder_map = {
            # 'Assets Liabilities': 'Assets_and_Liabilities',
            # 'Cash Flow': 'Cash_Flow',
            # 'Debt Management': 'Debt_Management',
            'Liquidity': 'Liquidity',
            # 'Operational Efficiency':
            # 'Investment_Efficiency'
            # 'Market Valuation': 'Market_Valuation',
            'Profitability': 'Profitability'
        }
        folder_name = query_to_folder_map.get(query_name)
        if not folder_name:
            self.error_handler.log(f"No folder mapping found for query {query_name}.", "ERROR")
            return None

        dir_path = os.path.join(self.local_storage_dir, str(self.cik_number), 'preprocessed_data', folder_name)
        if not os.path.isdir(dir_path):
            self.error_handler.log(f"Directory not found for query {query_name}.", "ERROR")
            return None

        try:
            files = [os.path.join(dir_path, f) for f in os.listdir(dir_path)]
            if not files:
                self.error_handler.log(f"No files found for query {query_name}.", "WARNING")
                return None

            files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            return files[0]
        except Exception as e:
            self.error_handler.log_error(e, "ERROR")
            return None

    def get_latest_processed_data_file_path(self, query_name):
        """
        Get the path of the latest processed data file for a specific query.
        Args:
            query_name (str): The name of the query.
        Returns:
            str: The path of the latest file, or None if no file is found.
        """
        query_to_folder_map = {
            'Liquidity': 'Liquidity',
            'Profitability': 'Profitability',
            # Add other categories as needed
        }
        folder_name = query_to_folder_map.get(query_name)
        if not folder_name:
            self.error_handler.log(f"No folder mapping found for query {query_name}.", "ERROR")
            return None

        dir_path = os.path.join(self.local_storage_dir, str(self.cik_number), 'processed_data', folder_name)
        if not os.path.isdir(dir_path):
            self.error_handler.log(f"Directory not found for query {query_name}.", "ERROR")
            return None

        try:
            files = [os.path.join(dir_path, f) for f in os.listdir(dir_path)]
            if not files:
                self.error_handler.log(f"No files found for query {query_name}.", "WARNING")
                return None

            files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            return files[0]
        except Exception as e:
            self.error_handler.log_error(e, "ERROR")
            return None
