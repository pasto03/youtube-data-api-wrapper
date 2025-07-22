from ..base import UniquePipe
from .params import VideosParams


class VideosPipe(UniquePipe):
    def __init__(self, params: VideosParams, developerKey: str, debug=False):
        super().__init__(params=params, developerKey=developerKey, debug=debug)
        self.pipe_fn = self.client.videos()