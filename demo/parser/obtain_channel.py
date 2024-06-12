"""
demo -- obtain channel details by channelId
"""
import sys_config
from utils import channel_fn

from src.channel.props import ChannelParams, ChannelCheckboxProps
from src.channel import ChannelResponse


params = ChannelParams(part=ChannelCheckboxProps(snippet=True, statistics=True).convert(), id="UC00EceQGGCMucNvwOS-jQ7A")

request = channel_fn.list(**params.to_dict())
response = request.execute()
# print(response["items"][0])

processed_response = ChannelResponse(response)

response_item_sample = processed_response.items[0]

print(processed_response.items[0])