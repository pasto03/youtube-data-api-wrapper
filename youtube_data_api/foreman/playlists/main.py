from youtube_data_api.retriever import PlaylistsRetriever
from youtube_data_api.container import PlaylistsContainer
from youtube_data_api.shipper import PlaylistShipper

from youtube_data_api.retriever.base import PipeSettings

from youtube_data_api.foreman.base import IterableForeman

class PlaylistsForeman(IterableForeman):
    """
    Retrieve playlist details given channelId(s) and convert to 1D dict.
    """
    def __init__(self):
        super().__init__()
        self.retriever = PlaylistsRetriever
        self.container = PlaylistsContainer
        self.shipper = PlaylistShipper
    
    def invoke(self, iterable: list[str], developerKey: str, 
               settings: PipeSettings = PipeSettings(), backup=True) -> PlaylistShipper:
        return super().invoke(iterable=iterable, developerKey=developerKey, settings=settings, backup=backup)