from ...retriever import RetrieverSettings, PlaylistItemsRetriever
from ...container import PlaylistItemsContainer
from ...shipper import PlaylistItemShipper

from ...retriever.base import PipeSettings
from ...foreman.base import IterableForeman


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
               pipe_settings: PipeSettings,
               retriever_settings = RetrieverSettings(output_folder="backup/PlaylistItemsRetriever"), 
               backup_shipper=True, max_workers: int = 8, debug: bool = False, as_box=False) -> PlaylistItemShipper | PlaylistItemsContainer:
        return super().invoke(iterable=iterable, developerKey=developerKey, pipe_settings=pipe_settings, 
                              retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
                              max_workers=max_workers, debug=debug, as_box=as_box)