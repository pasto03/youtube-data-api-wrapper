"""
PipeSettings is applicable to:
- PlaylistItemsRetriever
- PlaylistsRetriever
- SearchRetriever
"""
from youtube_data_api.retriever import PlaylistItemsRetriever, PlaylistsRetriever, SearchRetriever
from youtube_data_api.retriever.base import PipeSettings


# example 1: we want all items from first page only
settings = PipeSettings(retrieval="head", n=50)

# example 2: we want 10 items first page only
settings = PipeSettings(retrieval="custom", n=10)

# example 3: we want all items
settings = PipeSettings(retrieval="all")


worker = SearchRetriever(iterable=["90's China Pop songs"], developerKey="YOUR DEV KEY", settings=settings)
worker.invoke()