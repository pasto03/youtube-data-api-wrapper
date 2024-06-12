"""
demo -- search channel item by keyword
"""
import sys_config

from src.search.params import SearchParams
from src.search.channel import SearchChannelResponse
from utils import search_fn

import json

params = SearchParams(q="敬拜赞美", type="channel")

request = search_fn.list(**params.to_dict())
response = request.execute()

# print(json.dumps(response, indent=4, ensure_ascii=False))

processed_response = SearchChannelResponse(response)
print(processed_response.items[0])