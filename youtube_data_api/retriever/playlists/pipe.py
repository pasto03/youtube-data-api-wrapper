from ..base import IterablePipe, PipeSettings
from .params import PlaylistsParams

    
class PlaylistsPipe(IterablePipe):
    """
    Receive one channelId and return playlist resources
    Only PlaylistsRetriever is supposed to implement this object
    """
    def __init__(self, params: PlaylistsParams, pipe_fn=None, settings: PipeSettings = PipeSettings()):
        super().__init__(params=params, pipe_fn=pipe_fn, settings=settings)