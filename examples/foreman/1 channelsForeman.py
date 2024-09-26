from youtube_data_api.foreman import ChannelsForeman


# others foreman follow same procedure
channelIds = ["id1", "id2", ...]
foreman = ChannelsForeman()
shipper = foreman.invoke(iterable=channelIds, developerKey="YOUR DEV KEY")
records = shipper.main_records
thumbnails = shipper.thumbnails