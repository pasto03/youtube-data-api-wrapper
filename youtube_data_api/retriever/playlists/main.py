from ..base import IterableRetriever, PipeSettings
from .params import PlaylistsParams, PlaylistsCheckboxProps
from .pipe import PlaylistsPipe


class PlaylistsRetriever(IterableRetriever):
    """
    Retrieve playlists from a channel.

    Attributes
    ----------
    pipe_fn : any
        API to obtain response.
    pipe : PlaylistsPipe
        Pipe to process request by arguments.

    Parameters
    ----------
    iterable : list of str
        A list of channel IDs.
    developerKey : str
        API key obtained from Google Dev Console.
    settings : PipeSettings
        Determines how many pages of response to be obtained.
    """
    def __init__(self, iterable: list[str], developerKey: str, settings: PipeSettings = PipeSettings()):
        super().__init__(iterable=iterable, developerKey=developerKey, settings=settings)
        # these parameters need to be overwritten
        self.pipe_fn = self.client.playlists()
        self.pipe = PlaylistsPipe
    
    def _create_params(self, i):
        return PlaylistsParams(PlaylistsCheckboxProps().convert(), channelId=i)
    
    def invoke(self, output_folder="backup/PlaylistsRetriever", 
           filename=None, backup=True) -> list[dict]:
        return super().invoke(output_folder=output_folder, filename=filename, backup=backup)