from youtube_data_api.retriever import PlaylistItemsRetriever
from youtube_data_api.container import PlaylistItemsContainer
from youtube_data_api.shipper import PlaylistItemShipper

from youtube_data_api.retriever.base import PipeSettings
from youtube_data_api.foreman.base import IterableForeman

class PlaylistItemsForeman(IterableForeman):
    """
    Retrieve playlistItems given a playlistId and convert to 1D dict.
    """
    def __init__(self):
        super().__init__()
        self.retriever = PlaylistItemsRetriever
        self.container = PlaylistItemsContainer
        self.shipper = PlaylistItemShipper
    
    def invoke(self, iterable: list[str], developerKey: str, 
               settings: PipeSettings = PipeSettings(), backup=True) -> PlaylistItemShipper:
        return super().invoke(iterable=iterable, developerKey=developerKey, settings=settings, backup=backup)