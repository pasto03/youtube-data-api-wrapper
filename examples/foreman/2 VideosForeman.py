"""
retrieve video details given videoIds
"""
from youtube_data_api.foreman import VideosForeman


# others foreman follow same procedure
videoIds = ["id1", "id2", ...]
foreman = VideosForeman()
shipper = foreman.invoke(iterable=videoIds, developerKey="YOUR DEV KEY")
records = shipper.main_records
thumbnails = shipper.thumbnails