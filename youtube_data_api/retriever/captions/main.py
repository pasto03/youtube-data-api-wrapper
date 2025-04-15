from ..base import SingleRetriever
from .pipe import CaptionsPipe
from .params import CaptionsParams


class CaptionsRetriever(SingleRetriever):
    """
    Retrieve caption resource from given videoId

    Attributes
    ----------
    pipe_fn : any
        API to obtain response.
    pipe : CaptionsPipe
        Pipe to process request by arguments.

    Parameters
    ----------
    params : CaptionsParams
        CaptionsParams object as parameter.
    developerKey : str
        API key obtained from Google Dev Console.
    """
    def __init__(self, params: CaptionsParams, developerKey: str):
        super().__init__(params, developerKey)
        self.pipe_fn = self.client.captions()
        self.pipe = CaptionsPipe

    def invoke(self, output_folder="backup/CaptionsRetriever", 
            filename=None, backup=True) -> list[dict]:
        return super().invoke(output_folder=output_folder, filename=filename, backup=backup)