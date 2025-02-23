from ..base import PipeSettings, IterableRetriever
from .params import PlaylistItemsParams, PlaylistItemsCheckboxProps
from .pipe import PlaylistItemsPipe


class PlaylistItemsRetriever(IterableRetriever):
    """
    Retrieve videos (called playlistItems) from a playlist.

    Attributes
    ----------
    pipe_fn : any
        API to obtain response.
    pipe : PlaylistItemsPipe
        Pipe to process request by arguments.

    Parameters
    ----------
    iterable : list of str
        A list of playlist IDs.
    developerKey : str
        API key obtained from Google Dev Console.
    settings : PipeSettings
        Determines how many pages of response to be obtained.
    """

    def __init__(self, iterable: list[str], developerKey: str, settings: PipeSettings = PipeSettings()):
        super().__init__(iterable=iterable, developerKey=developerKey, settings=settings)
        # these parameters need to be overwritten
        self.pipe_fn = self.client.playlistItems()
        self.pipe = PlaylistItemsPipe
    
    def _create_params(self, i):
        return PlaylistItemsParams(PlaylistItemsCheckboxProps().convert(), playlistId=i)
    
    def invoke(self, output_folder="backup/PlaylistItemsRetriever", 
           filename=None, backup=True) -> list[dict]:
        return super().invoke(output_folder=output_folder, filename=filename, backup=backup)