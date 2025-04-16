from ..base import IterablePipe, PipeSettings
from .params import PlaylistsParams

    
class PlaylistsPipe(IterablePipe):
    """
    Receive one channelId and return playlist resources
    Only PlaylistsRetriever is supposed to implement this object
    """
    def __init__(self, params: PlaylistsParams, settings: PipeSettings):
        super().__init__(params=params, settings=settings)