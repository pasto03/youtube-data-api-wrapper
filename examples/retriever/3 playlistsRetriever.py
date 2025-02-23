from youtube_data_api.retriever.playlists import PlaylistsRetriever


channelIds = ["id1", "id2", ...]
worker = PlaylistsRetriever(iterable=channelIds, developerKey="YOUR DEV KEY")
worker.invoke()