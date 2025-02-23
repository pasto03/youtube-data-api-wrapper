from youtube_data_api.retriever import ChannelsRetriever


channelIds = ["id1", "id2", ...]
worker = ChannelsRetriever(iterable=channelIds, developerKey="YOUR DEV KEY")
worker.invoke()