from typing import TypeAlias, Literal
from tqdm import tqdm
import math

from ..base.pipe import BasePipe
from .params import SearchParams


RetrieveMethod: TypeAlias = Literal["head", "custom", "all"]


class SearchPipe(BasePipe):
    """
    Receive parameters and return search resources
    Only SearchRetriever is supposed to implement this object
    """
    def __init__(self, params: SearchParams, pipe_fn=None, 
             retrieval: RetrieveMethod = "head", n=10):
        super().__init__(params=params, pipe_fn=pipe_fn, retrieval=retrieval, n=n)
        self.max_page = 5
    
    def _get_all_response(self):
        return super()._get_all_response(max_page=self.max_page)