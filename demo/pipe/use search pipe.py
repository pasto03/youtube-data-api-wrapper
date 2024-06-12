import sys_config

from src.pipeline.pipe import SearchPipe

import json

pipe = SearchPipe(retrieval="head", q="敬拜赞美", order="viewCount", type="playlist")

responses = pipe.run_pipe()
print(responses)

# with open("data records/search playlist 2.json", "wb") as f:
#     f.write(json.dumps({"result": responses}, indent=4, ensure_ascii=False).encode("utf-8"))