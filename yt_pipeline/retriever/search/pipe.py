from ..base import IterablePipe, PipeSettings
from .params import SearchParams


class SearchPipe(IterablePipe):
    """
    Receive parameters and return search resources
    """
    def __init__(self, params: SearchParams, developerKey: str, settings: PipeSettings = PipeSettings(), debug=False):
        super().__init__(params=params, developerKey=developerKey, settings=settings, debug=debug)
        self.pipe_fn = self.client.search()