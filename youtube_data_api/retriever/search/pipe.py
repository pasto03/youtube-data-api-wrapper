from ..base import IterablePipe, PipeSettings
from .params import SearchParams


class SearchPipe(IterablePipe):
    """
    Receive parameters and return search resources
    Only SearchRetriever is supposed to implement this object
    """
    def __init__(self, params: SearchParams, pipe_fn=None, settings: PipeSettings = PipeSettings):
        super().__init__(params=params, pipe_fn=pipe_fn, settings=settings)