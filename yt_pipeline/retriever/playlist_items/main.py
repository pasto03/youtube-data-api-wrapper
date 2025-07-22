from ..base import PipeSettings, IterableRetriever
from .params import PlaylistItemsParams, PlaylistItemsCheckboxProps
from .pipe import PlaylistItemsPipe


class PlaylistItemsRetriever(IterableRetriever):
    """
    Retrieve videos (called playlistItems) from a playlist.

    Parameters
    ----------
    iterable : list of str
        A list of playlist IDs.
    developerKey : str
        API key obtained from Google Dev Console.
    settings : PipeSettings
        Determines how many pages of response to be obtained.
    """

    def __init__(self, iterable: list[str], developerKey: str, settings: PipeSettings = PipeSettings(), 
                 max_workers=8, debug=False):
        super().__init__(iterable=iterable, developerKey=developerKey, settings=settings, max_workers=max_workers, debug=debug)
        self.pipe = PlaylistItemsPipe
    
    def _create_params(self, i: str):
        return PlaylistItemsParams(PlaylistItemsCheckboxProps().convert(), playlistId=i)
    
    def invoke(self, output_folder="backup/PlaylistItemsRetriever", flatten_result=True,
           filename=None, backup=True, backup_when_halted=False, multithread=False):
        return super().invoke(output_folder=output_folder, flatten_result=flatten_result, filename=filename, backup=backup, backup_when_halted=backup_when_halted, multithread=multithread)