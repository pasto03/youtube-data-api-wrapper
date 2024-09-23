from ..base import PipeSettings, BaseRetriever
from .params import PlaylistItemsParams, PlaylistItemsCheckboxProps
from .pipe import PlaylistItemsPipe


class PlaylistItemsRetriever(BaseRetriever):
    def __init__(self, iterable: list[str], developerKey: str, settings: PipeSettings = PipeSettings()):
        super().__init__(iterable=iterable, developerKey=developerKey, settings=settings)
        # these parameters need to be overwritten
        self.pipe_fn = self.client.playlistItems()
        self.pipe = PlaylistItemsPipe
    
    def _create_params(self, i):
        return PlaylistItemsParams(PlaylistItemsCheckboxProps().convert(), playlistId=i)
    
    def invoke(self, output_folder="backup/PlaylistItemsRetriever", 
           filename=None, backup=True, progress_bar=True) -> list[dict]:
        return super().invoke(output_folder=output_folder, filename=filename, backup=backup, progress_bar=progress_bar)