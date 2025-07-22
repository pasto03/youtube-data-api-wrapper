from ..base import UniquePipe
from .params import VideoCategoriesParams


class VideoCategoriesPipe(UniquePipe):
    def __init__(self, params: VideoCategoriesParams, developerKey: str, debug=False):
        super().__init__(params=params, developerKey=developerKey, debug=debug)
        self.pipe_fn = self.client.videoCategories()