from youtube_data_api.retriever import CommentThreadsRetriever
from youtube_data_api.container import CommentThreadsContainer
from youtube_data_api.shipper import CommentThreadsShipper

from youtube_data_api.retriever.base import PipeSettings
from youtube_data_api.foreman.base import IterableForeman


class CommentThreadsForeman(IterableForeman):
    """
    Retrieve comment threads and replies given videoId
    """
    def __init__(self):
        super().__init__()
        self.retriever = CommentThreadsRetriever
        self.container = CommentThreadsContainer
        self.shipper = CommentThreadsShipper
    
    def invoke(self, iterable: list[str], developerKey: str, 
               settings: PipeSettings = PipeSettings(), backup=True) -> CommentThreadsShipper:
        return super().invoke(iterable=iterable, developerKey=developerKey, settings=settings, backup=backup)