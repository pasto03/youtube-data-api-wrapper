"""
retrieve comment threads and replies given videoIds
"""
from youtube_data_api.foreman import CommentThreadsForeman
from youtube_data_api.retriever.base import PipeSettings


foreman = CommentThreadsForeman()
shipper = foreman.invoke(iterable=["videoId1", "videoId2", ...], developerKey="DEVKEY", 
               settings=PipeSettings(retrieval="all", max_page=2))
# Note: main_records = comment_threads
# records = shipper.main_records
comment_threads = shipper.comment_threads
replies = shipper.replies