"""
demo -- search video item by keyword
"""
import sys_config

from src.search.params import SearchParams
from src.search.video import SearchVideoResponse
from utils import search_fn

import json

params = SearchParams(q="赞美之泉", type='video')

request = search_fn.list(**params.to_dict())
response = request.execute()

print(json.dumps(response, indent=4, ensure_ascii=False))

processed_response = SearchVideoResponse(response)
print(processed_response.items[0])