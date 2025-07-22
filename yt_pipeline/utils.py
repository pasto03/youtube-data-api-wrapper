

def split_list(input_list, chunk_size=50):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def flatten_chain(obj: list[list]):
    from itertools import chain
    return list(chain.from_iterable(obj))

def dict_to_json(json_dict: list[dict] | dict) -> str:
    import json
    return json.dumps(json_dict, indent=4, ensure_ascii=False)

def get_current_time():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H-%M-%S')

def build_client(developerKey):
    from googleapiclient.discovery import build
    client = build('youtube', 'v3', developerKey=developerKey)
    return client

def handle_backup(raw_items: list[dict], output_folder="backup/Backups", filename=None):
    import os

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not filename:
        filename = get_current_time() + ".json"
    records = dict_to_json(raw_items)
    with open(os.path.join(output_folder, filename), "wb") as f:
        f.write(records.encode("utf-8"))
