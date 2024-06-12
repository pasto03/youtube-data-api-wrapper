import sys_config
from src.pipeline.pipe import ChannelPipe

import json

pipe = ChannelPipe(channelId="UC00EceQGGCMucNvwOS-jQ7A")

responses = pipe.run_pipe()
print(responses)