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
        self.name = "comment_threads"

    def _pack(self, raw_items: list[dict]) -> CommentThreadsContainer:
        return super()._pack(raw_items)
    
    def _ship(self, box: CommentThreadsContainer, backup=True) -> CommentThreadsShipper:
        return super()._ship(box, backup)
    
    def invoke(self, iterable: list[str], developerKey: str, 
               settings: PipeSettings = PipeSettings(), backup=True, as_box=False) -> CommentThreadsShipper | CommentThreadsContainer:
        return super().invoke(iterable=iterable, developerKey=developerKey, settings=settings, backup=backup, as_box=as_box)