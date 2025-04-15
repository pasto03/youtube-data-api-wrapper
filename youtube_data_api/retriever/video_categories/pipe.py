from ..base import UniquePipe
from .params import VideoCategoriesParams


class VideoCategoriesPipe(UniquePipe):
    def __init__(self, params: VideoCategoriesParams, pipe_fn=None):
        super().__init__(params, pipe_fn)