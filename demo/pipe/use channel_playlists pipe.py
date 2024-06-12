import sys_config

from src.pipeline.pipe import ChannelPlaylistPipe

import json

pipe = ChannelPlaylistPipe(retrieval="all", channelId="UC00EceQGGCMucNvwOS-jQ7A")

responses = pipe.run_pipe()

with open("data records/channel_playlists/channel playlist 1.json", "wb") as f:
    f.write(json.dumps({"result": responses}, indent=4, ensure_ascii=False).encode("utf-8"))