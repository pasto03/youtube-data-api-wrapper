"""
retrieve caption tracks associated with specified videoId

Note: This foreman may be removed in the future updates
"""
from youtube_data_api.foreman import CaptionsForeman


foreman = CaptionsForeman()
shipper = foreman.invoke(videoId="videoId", developerKey="DEVKEY")
records = shipper.main_records