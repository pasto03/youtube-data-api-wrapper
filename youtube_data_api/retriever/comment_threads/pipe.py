from typing import TypeAlias, Literal
from tqdm import tqdm
import math

from ..base import IterablePipe
from .params import CommentThreadsParams

RetrieveMethod: TypeAlias = Literal["head", "custom", "all"]
    

class CommentThreadsPipe(IterablePipe):
    """
    obtain list of comment threads given a videoId
    """
    def __init__(self, params: CommentThreadsParams, pipe_fn=None, 
                 retrieval: RetrieveMethod = "head", n=10):
        super().__init__(params=params, pipe_fn=pipe_fn, retrieval=retrieval, n=n)
        self.hard_limit = 100    # this API allows up to 100 results per page
        self.max_page = 5   # limitation for pipe to avoid using too much quota
    
    def _get_all_response(self):
        return super()._get_all_response(max_page=self.max_page)