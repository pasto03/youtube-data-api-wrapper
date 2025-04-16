from ..base import IterablePipe, PipeSettings
from .params import PlaylistItemsParams


class PlaylistItemsPipe(IterablePipe):
    """
    obtain playlistItems by a playlistId
    Only PlaylistItemsWorker is supposed to implement this object
    """
    def __init__(self, params: PlaylistItemsParams, pipe_fn=None, settings: PipeSettings = PipeSettings()):
        super().__init__(params=params, pipe_fn=pipe_fn, settings=settings)