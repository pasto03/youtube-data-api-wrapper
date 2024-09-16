

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

