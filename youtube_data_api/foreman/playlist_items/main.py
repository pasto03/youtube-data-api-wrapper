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
        self.name = "playlist_items"

    def _pack(self, raw_items) -> PlaylistItemsContainer:
        return super()._pack(raw_items)
    
    def _ship(self, box, backup=True) -> PlaylistItemShipper:
        return super()._ship(box, backup)
    
    def invoke(self, iterable: list[str], developerKey: str, 
               settings: PipeSettings = PipeSettings(), backup=True, as_box=False) -> PlaylistItemShipper | PlaylistItemsContainer:
        return super().invoke(iterable=iterable, developerKey=developerKey, settings=settings, backup=backup, as_box=as_box)