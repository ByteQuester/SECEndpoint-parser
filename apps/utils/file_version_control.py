import os
import pandas as pd


class FileVersionManager:
    def __init__(self, base_dir='data'):
        self.base_dir = base_dir

    def compare_dataframes(self, df1, df2):
        """
        Compare two DataFrames to determine if they are different.
        Returns True if different, False otherwise.
        """
        # Simple comparison for now to check if the DataFrames are identical
        return not df1.equals(df2)

    def check_and_update_file(self, cik_number, query_name, new_data, timestamp):
        cik_folder = str(int(cik_number))
        query_dir = os.path.join(self.base_dir, cik_folder, query_name.replace(' ', '_'))
        file_name = f"{cik_number}_{query_name.replace(' ', '_')}_{timestamp}.csv"
        file_path = os.path.join(query_dir, file_name)

        if os.path.exists(file_path):
            existing_data = pd.read_csv(file_path)
            if self.compare_dataframes(existing_data, new_data):
                new_data.to_csv(file_path, index=False)
                return file_path, True  # File updated

        new_data.to_csv(file_path, index=False)
        return file_path, False

    def update_index_file(self, cik_number, query_name, file_path):
        cik_folder = str(int(cik_number))
        index_file_path = os.path.join(self.base_dir, cik_folder, 'index.md')
        section_title = f"### {query_name}\n"

        # Check if the index file is being created for the first time
        if not os.path.exists(index_file_path):
            with open(index_file_path, 'w') as index_file:
                index_file.write(f"---\ntitle: CIK {cik_number} Data\nslug: /data/{cik_folder}\n---\n\n")

        # Check if the section already exists
        if not self._section_exists(index_file_path, section_title):
            with open(index_file_path, 'a') as index_file:
                index_file.write(f"\n{section_title}")

        entry = f"- [{query_name} {file_path.split('_')[-1].split('.')[0]}]({file_path})\n"
        with open(index_file_path, 'a') as index_file:
            index_file.write(entry)

    def _section_exists(self, index_file_path, section_title):
        if not os.path.exists(index_file_path):
            return False
        with open(index_file_path, 'r') as index_file:
            return section_title in index_file.read()