from ..base import IterablePipe, PipeSettings
from .params import PlaylistsParams

    
class PlaylistsPipe(IterablePipe):
    """
    Receive one channelId and return playlist resources
    """
    def __init__(self, params: PlaylistsParams, developerKey: str, settings: PipeSettings = PipeSettings(), debug=False):
        super().__init__(params=params, developerKey=developerKey, settings=settings, debug=debug)
        self.pipe_fn = self.client.playlists()