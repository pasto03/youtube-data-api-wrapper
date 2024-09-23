from ..base import UniqueRetriever
from .pipe import VideosPipe
from .params import VideosParams, VideosCheckboxProps


class VideosRetriever(UniqueRetriever):
    def __init__(self, iterable: list[str], developerKey: str):
        super().__init__(iterable, developerKey)
        self.pipe_fn = self.client.videos()
        self.pipe = VideosPipe
    
    def _create_params(self, chunk):
        chunk = ",".join(chunk)
        return VideosParams(VideosCheckboxProps().convert(), id=chunk)
    
    def invoke(self, output_folder="backup/VideosRetriever", 
               filename=None, backup=True, progress_bar=True) -> list[dict]:
        return super().invoke(output_folder=output_folder, filename=filename, backup=backup, progress_bar=progress_bar)