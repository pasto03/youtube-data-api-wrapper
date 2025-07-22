from ..base import IterableRetriever, PipeSettings
from .params import PlaylistsParams, PlaylistsCheckboxProps
from .pipe import PlaylistsPipe


class PlaylistsRetriever(IterableRetriever):
    """
    Retrieve playlists from a channel.

    Parameters
    ----------
    iterable : list of str
        A list of channel IDs.
    developerKey : str
        API key obtained from Google Dev Console.
    settings : PipeSettings
        Determines how many pages of response to be obtained.
    """
    def __init__(self, iterable: list[str], developerKey: str, settings: PipeSettings = PipeSettings(), 
                 max_workers=8, debug=False):
        super().__init__(iterable=iterable, developerKey=developerKey, settings=settings, max_workers=max_workers, debug=debug)
        self.pipe = PlaylistsPipe
    
    def _create_params(self, i):
        return PlaylistsParams(PlaylistsCheckboxProps().convert(), channelId=i)
    
    def invoke(self, output_folder="backup/PlaylistsRetriever", flatten_result=True,
           filename=None, backup=True, backup_when_halted=False, multithread=False):
        return super().invoke(output_folder=output_folder, flatten_result=flatten_result, filename=filename, backup=backup, backup_when_halted=backup_when_halted, multithread=multithread)