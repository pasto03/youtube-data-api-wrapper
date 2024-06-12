import sys_config
from src.pipeline.pipe import VideoPipe

import json

pipe = VideoPipe(videoId="bgun_D8_jGw")

responses = pipe.run_pipe()
print(responses)