from ..base import UniquePipe
from .params import CaptionsParams


class CaptionsPipe(UniquePipe):
    def __init__(self, params: CaptionsParams, pipe_fn=None):
        super().__init__(params, pipe_fn)