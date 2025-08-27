from ..base import UniquePipe
from .params import CaptionsParams


class CaptionsPipe(UniquePipe):
    def __init__(self, params: CaptionsParams, developerKey: str, debug=False):
        super().__init__(params, developerKey=developerKey, debug=debug)
        self.pipe_fn = self.client.captions()