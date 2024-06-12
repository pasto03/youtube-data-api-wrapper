"""
demo -- obtain video details by videoId
"""
import sys_config
from utils import video_fn

from src.video.props import VideosCheckboxProps
from src.video.params import VideosParams

from src.video import VideoResponse


params = VideosParams(
    part=VideosCheckboxProps(contentDetails=True, snippet=True, statistics=True).convert(), 
    id="pSY3i5XHHXo"
)

request = video_fn.list(**params.to_dict())
response = request.execute()


processed_response = VideoResponse(response)

response_item_sample = processed_response.items[0]

print(processed_response.items[0])