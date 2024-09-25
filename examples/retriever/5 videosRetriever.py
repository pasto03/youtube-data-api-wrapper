from youtube_data_api.retriever import VideosRetriever


videoIds = ["id1", "id2", ...]
worker = VideosRetriever(iterable=videoIds, developerKey="YOUR DEV KEY")
worker.invoke()