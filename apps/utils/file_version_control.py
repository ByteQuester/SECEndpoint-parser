import os


class FileVersionManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def update_index(self, cik_number, category, file_name, storage_type):
        index_path = os.path.join(self.base_dir, cik_number, storage_type, 'index.md')
        self._write_to_index(index_path, cik_number, category, file_name, storage_type)

    def _write_to_index(self, index_path, cik_number, category, file_name, storage_type):
        # Ensure the directory for the index file exists
        os.makedirs(os.path.dirname(index_path), exist_ok=True)

        index_content = self._read_index(index_path)
        formatted_category = category.replace(' ', '_')
        relative_path = f"data/{cik_number}/{storage_type}/{formatted_category}/{file_name}"
        index_content[f"### {category}"] = f"- [{category} {file_name.split('_')[-1].split('.')[0]}]({relative_path})\n"
        self._save_index(index_path, cik_number,storage_type, index_content)

    def _read_index(self, index_path):
        if not os.path.exists(index_path):
            return {}

        with open(index_path, 'r') as file:
            lines = file.readlines()

        index_content = {}
        current_category = None
        for line in lines:
            if line.startswith('### '):  # Category line
                current_category = line.strip()
                index_content[current_category] = ''
            elif current_category and line.strip():
                # Append file entry to current category
                index_content[current_category] += line
        return index_content

    def _save_index(self, index_path, cik_number, storage_type, index_content):
        with open(index_path, 'w') as file:
            file.write(f"---\ntitle: CIK {cik_number} Data\nslug: /data/{cik_number}/{storage_type}/\n---\n\n")
            for category, entry in index_content.items():
                file.write(f"{category}\n{entry}\n")
