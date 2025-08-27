from ...retriever import RetrieverSettings, CommentThreadsRetriever
from ...container import CommentThreadsContainer
from ...shipper import CommentThreadsShipper

from ...retriever.base import PipeSettings
from ...foreman.base import IterableForeman


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
    
    def _ship(self, box: CommentThreadsContainer, backup=False) -> CommentThreadsShipper:
        return super()._ship(box, backup)
    
    def invoke(self, iterable: list[str], developerKey: str,
               pipe_settings: PipeSettings,
               retriever_settings = RetrieverSettings(output_folder="backup/CommentThreadsRetriever"), 
               backup_shipper=True, max_workers: int = 8, debug: bool = False, as_box=False) -> CommentThreadsShipper | CommentThreadsContainer:
        return super().invoke(iterable=iterable, developerKey=developerKey, pipe_settings=pipe_settings, 
                              retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
                              max_workers=max_workers, debug=debug, as_box=as_box)