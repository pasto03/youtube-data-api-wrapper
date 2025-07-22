from ..base import IterablePipe, PipeSettings
from .params import PlaylistItemsParams


class PlaylistItemsPipe(IterablePipe):
    """
    obtain playlistItems by a playlistId
    """
    def __init__(self, params: PlaylistItemsParams, developerKey: str, settings: PipeSettings = PipeSettings(), debug=False):
        super().__init__(params=params, developerKey=developerKey, settings=settings, debug=debug)
        self.pipe_fn = self.client.playlistItems()