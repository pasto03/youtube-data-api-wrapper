from youtube_data_api.retriever.playlist_items import PlaylistItemsRetriever


playlistIds = ["id1", "id2", ...]
worker = PlaylistItemsRetriever(iterable=playlistIds, developerKey="YOUR DEV KEY")
worker.invoke()