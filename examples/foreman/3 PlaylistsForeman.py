"""
retrieve playlists given channelIds
"""
from youtube_data_api.foreman import PlaylistsForeman
from youtube_data_api.retriever.base import PipeSettings


foreman = PlaylistsForeman()
shipper = foreman.invoke(iterable=["channelId1", "channelId2", ...], developerKey="DEVKEY", 
               settings=PipeSettings(retrieval="all", max_page=5))
records = shipper.main_records