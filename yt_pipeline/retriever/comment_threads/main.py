from dataclasses import asdict

from ..base import PipeSettings, IterableRetriever
from .params import CommentThreadsParams, CommentThreadParamProps
from .pipe import CommentThreadsPipe
from ...container import HttpErrorContainer


class CommentThreadsRetriever(IterableRetriever):
    """
    Retrieve comment threads by videoId(s)

    Parameters
    ----------
    iterable : list of str
        A list of video IDs.
    developerKey : str
        API key obtained from Google Dev Console.
    settings : PipeSettings
        Determines how many pages of response to be obtained.
    """

    def __init__(self, iterable: list[str], developerKey: str, 
                 settings: PipeSettings = PipeSettings(),
                 props: CommentThreadParamProps = CommentThreadParamProps(), 
                 max_workers=8, debug=False):
        super().__init__(iterable=iterable, developerKey=developerKey, settings=settings, max_workers=max_workers, debug=debug)
        # these parameters need to be overwritten
        self.props = props
        self.pipe = CommentThreadsPipe
        
    def _create_params(self, i: str):
        return CommentThreadsParams(**asdict(self.props), videoId=i)
    
    def invoke(self, output_folder="backup/CommentThreadsRetriever", flatten_result=True,
           filename=None, backup=True, backup_when_halted=False, multithread=False):
        return super().invoke(output_folder=output_folder, flatten_result=flatten_result, filename=filename, backup=backup, backup_when_halted=backup_when_halted, multithread=multithread)