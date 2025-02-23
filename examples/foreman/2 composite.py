"""
multiple foremen works together

Objective: obtain channel details from given channel names(keywords)
"""
from youtube_data_api.foreman import SearchForeman, ChannelsForeman
from youtube_data_api.container import SearchContainer
from youtube_data_api.retriever.search.params import SearchTypeCheckboxProps


developerKey = "YOUR DEV KEY"

# 1. obtain corresponding channelIds
keywords = ["k1", "k2", ...]
types = SearchTypeCheckboxProps(channel=True, playlist=False, video=False)   # we want channel results only
foreman1 = SearchForeman()
shipper1 = foreman1.invoke(iterable=keywords, developerKey=developerKey, types=types)
records1 = shipper1.main_records


# 2. obtain channel details
channelIds = [i['channelId'] for i in records1]   # check key from corresponding container object
foreman2 = ChannelsForeman()
shipper2 = foreman2.invoke(iterable=channelIds, developerKey=developerKey)

# final outputs here
records2 = shipper2.main_records