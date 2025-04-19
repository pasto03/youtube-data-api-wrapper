from ..base import IterablePipe, PipeSettings
from .params import CommentThreadsParams
    

class CommentThreadsPipe(IterablePipe):
    """
    obtain list of comment threads given a videoId
    """
    def __init__(self, params: CommentThreadsParams, pipe_fn=None, settings: PipeSettings = PipeSettings()):
        super().__init__(params=params, pipe_fn=pipe_fn, settings=settings)
        self.hard_limit = 100    # this API allows up to 100 results per page

    def _get_all_response(self):
        return super()._get_all_response(infinite_query=True)