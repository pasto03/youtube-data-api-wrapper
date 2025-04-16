from ..base import PipeSettings, IterableRetriever
from .params import CommentThreadsParams
from .pipe import CommentThreadsPipe


class CommentThreadsRetriever(IterableRetriever):
    """
    Retrieve comment threads of a specific video

    Attributes
    ----------
    pipe_fn : any
        API to obtain response.
    pipe : CommentThreadsPipe
        Pipe to process request by arguments.

    Parameters
    ----------
    iterable : list of str
        A list of video IDs.
    developerKey : str
        API key obtained from Google Dev Console.
    settings : PipeSettings
        Determines how many pages of response to be obtained.
    """

    def __init__(self, iterable: list[str], developerKey: str, settings: PipeSettings = PipeSettings()):
        super().__init__(iterable=iterable, developerKey=developerKey, settings=settings)
        # these parameters need to be overwritten
        self.pipe_fn = self.client.commentThreads()
        self.pipe = CommentThreadsPipe
    
    def _create_params(self, i):
        return CommentThreadsParams(maxResults=100, videoId=i)
    
    def invoke(self, output_folder="backup/CommentThreadsRetriever", 
           filename=None, backup=True) -> list[dict]:
        return super().invoke(output_folder=output_folder, filename=filename, backup=backup)