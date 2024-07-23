import json


def write_to_json(data_path: str, data):
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
