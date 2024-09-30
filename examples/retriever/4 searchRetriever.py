from youtube_data_api.retriever import SearchRetriever


worker = SearchRetriever(iterable=["90's China Pop songs"], developerKey="YOUR DEV KEY")
worker.invoke()