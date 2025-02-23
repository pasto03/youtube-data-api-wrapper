from ..base import UniqueRetriever
from .pipe import VideosPipe
from .params import VideosParams, VideosCheckboxProps


class VideosRetriever(UniqueRetriever):
    """
    Retrieve video details.

    Attributes
    ----------
    pipe_fn : any
        API to obtain response.
    pipe : VideosPipe
        Pipe to process request by arguments.

    Parameters
    ----------
    iterable : list of str
        A list of video IDs.
    developerKey : str
        API key obtained from Google Dev Console.
    """
    def __init__(self, iterable: list[str], developerKey: str):
        super().__init__(iterable, developerKey)
        self.pipe_fn = self.client.videos()
        self.pipe = VideosPipe
    
    def _create_params(self, chunk):
        chunk = ",".join(chunk)
        return VideosParams(VideosCheckboxProps().convert(), id=chunk)
    
    def invoke(self, output_folder="backup/VideosRetriever", 
               filename=None, backup=True) -> list[dict]:
        return super().invoke(output_folder=output_folder, filename=filename, backup=backup)