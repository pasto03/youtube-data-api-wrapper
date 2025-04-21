"""
retrieve playlist items given playlistIds
"""
from youtube_data_api.foreman import PlaylistItemsForeman
from youtube_data_api.retriever.base import PipeSettings


foreman = PlaylistItemsForeman()
shipper = foreman.invoke(iterable=["playlistId1", "playlistId2", ...], developerKey="DEVKEY", 
               settings=PipeSettings(retrieval="all", max_page=5))
records = shipper.main_records