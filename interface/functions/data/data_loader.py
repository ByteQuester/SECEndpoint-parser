import pandas as pd
import os


class DataLoader:
    def __init__(self, base_dir='data'):
        self.base_dir = base_dir

    def construct_file_path(self, cik, query_type):
        folder_path = os.path.join(self.base_dir, str(cik), query_type)
        files = os.listdir(folder_path)
        if files:
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
            return os.path.join(folder_path, latest_file)
        return None

    def load_data(self, file_path):
        if file_path and os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                return df
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        else:
            print(f"File path is invalid: {file_path}")
        return None

# Example usage
# ## data_loader = DataLoader()
#     cik = 12927
#     query_type = 'profitability'
#     file_path = data_loader.construct_file_path(cik, query_type)
#     data = data_loader.load_data(file_path)


