import sys_config

from src.pipeline.pipe import PlaylistItemsPipe

import json

pipe = PlaylistItemsPipe(retrieval="head", playlistId="PLmRtGsDjFMjsVTsgcofhLG3ylXSOuE2q1")

responses = pipe.run_pipe()
# print(responses)

with open("data records/playlist_items/get playlists 1.json", "wb") as f:
    f.write(json.dumps({"result": responses}, indent=4, ensure_ascii=False).encode("utf-8"))