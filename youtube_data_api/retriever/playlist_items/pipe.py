from typing import TypeAlias, Literal
from tqdm import tqdm
import math

from ..base import IterablePipe
from .params import PlaylistItemsParams

RetrieveMethod: TypeAlias = Literal["head", "custom", "all"]
    
    
class PlaylistItemsPipe(IterablePipe):
    """
    obtain playlistItems by a playlistId
    Only PlaylistItemsWorker is supposed to implement this object
    """
    def __init__(self, params: PlaylistItemsParams, pipe_fn=None, 
                 retrieval: RetrieveMethod = "head", n=10):
        super().__init__(params=params, pipe_fn=pipe_fn, retrieval=retrieval, n=n)