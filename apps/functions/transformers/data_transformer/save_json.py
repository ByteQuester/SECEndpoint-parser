import json


def save_json(json_data, file_path):
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)