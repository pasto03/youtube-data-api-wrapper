"""
obtain playlists of a channel
"""
from youtube_data_api.foreman import SearchForeman
from youtube_data_api.retriever.search.params import SearchTypeCheckboxProps, SearchParamProps
from youtube_data_api.retriever.base import PipeSettings

developerKey = "YOUR DEV KEY"

channelIds = ["UCeOxIcPOMW4jO64C2lTSl-w", "UC7kIJ3kuhr1zMYQU4R67Iyw"]
foreman = SearchForeman()
iterable = [SearchParamProps(q="敬拜赞美", channelId=channelId, order="date", publishedAfter="2020-01-01T00:00:00Z") for channelId in channelIds]
shipper = foreman.invoke(iterable, types=SearchTypeCheckboxProps(channel=False, playlist=True, video=False), settings=PipeSettings(retrieval="head"), developerKey=developerKey)
print(shipper.main_records)