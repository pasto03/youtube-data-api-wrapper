from typing import TypeAlias, Literal
from tqdm import tqdm
import math


from ..base import IterablePipe
from .params import PlaylistsParams

RetrieveMethod: TypeAlias = Literal["head", "custom", "all"]
    
    
class PlaylistsPipe(IterablePipe):
    """
    Receive one channelId and return playlist resources
    Only PlaylistsRetriever is supposed to implement this object
    """
    def __init__(self, params: PlaylistsParams, pipe_fn=None, 
             retrieval: RetrieveMethod = "head", n=10):
        super().__init__(params=params, pipe_fn=pipe_fn, retrieval=retrieval, n=n)