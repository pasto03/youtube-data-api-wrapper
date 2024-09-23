from ..base import BaseRetriever, PipeSettings
from .params import PlaylistsParams, PlaylistsCheckboxProps
from .pipe import PlaylistsPipe


class PlaylistsRetriever(BaseRetriever):
    def __init__(self, iterable: list[str], developerKey: str, settings: PipeSettings = PipeSettings()):
        super().__init__(iterable=iterable, developerKey=developerKey, settings=settings)
        # these parameters need to be overwritten
        self.pipe_fn = self.client.playlists()
        self.pipe = PlaylistsPipe
    
    def _create_params(self, i):
        return PlaylistsParams(PlaylistsCheckboxProps().convert(), channelId=i)
    
    def invoke(self, output_folder="backup/PlaylistsRetriever", 
           filename=None, backup=True, progress_bar=True) -> list[dict]:
        return super().invoke(output_folder=output_folder, filename=filename, backup=backup, progress_bar=progress_bar)