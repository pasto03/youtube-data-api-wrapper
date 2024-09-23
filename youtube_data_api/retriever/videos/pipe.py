from ..base import UniquePipe
from .params import VideosParams


class VideosPipe(UniquePipe):
    def __init__(self, params: VideosParams, pipe_fn=None):
        super().__init__(params, pipe_fn)