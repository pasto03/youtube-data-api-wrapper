from ...retriever import RetrieverSettings, PlaylistsRetriever
from ...container import PlaylistsContainer
from ...shipper import PlaylistShipper

from ...retriever.base import PipeSettings

from ...foreman.base import IterableForeman

class PlaylistsForeman(IterableForeman):
    """
    Retrieve playlist details given channelId(s) and convert to 1D dict.
    """
    def __init__(self):
        super().__init__()
        self.retriever = PlaylistsRetriever
        self.container = PlaylistsContainer
        self.shipper = PlaylistShipper
        self.name = "playlists"

    def _pack(self, raw_items) -> PlaylistsContainer:
        return super()._pack(raw_items)
    
    def _ship(self, box, backup=True) -> PlaylistShipper:
        return super()._ship(box, backup)
    
    def invoke(self, iterable: list[str], developerKey: str,
               pipe_settings: PipeSettings,
               retriever_settings = RetrieverSettings(output_folder="backup/PlaylistsRetriever"), 
               backup_shipper=True, max_workers: int = 8, debug: bool = False, as_box=False) -> PlaylistShipper | PlaylistsContainer:
        return super().invoke(iterable=iterable, developerKey=developerKey, pipe_settings=pipe_settings, 
                              retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
                              max_workers=max_workers, debug=debug, as_box=as_box)