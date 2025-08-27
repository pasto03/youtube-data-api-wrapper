from ...retriever import RetrieverSettings, VideosRetriever
from ...container import VideosContainer
from ...shipper import VideoShipper

from ...foreman.base import UniqueForeman


class VideosForeman(UniqueForeman):
    """
    Retrieve video details given videoId(s) and convert to 1D dict.
    """
    def __init__(self):
        super().__init__()
        self.retriever = VideosRetriever
        self.container = VideosContainer
        self.shipper = VideoShipper
        self.name = "videos"

    def _pack(self, raw_items) -> VideosContainer:
        return super()._pack(raw_items)
    
    def _ship(self, box, backup=False) -> VideoShipper:
        return super()._ship(box, backup)

    def invoke(self, iterable: list[str], developerKey: str, 
               retriever_settings = RetrieverSettings(output_folder="backup/VideosRetriever"), 
               backup_shipper=True, max_workers: int = 8, debug: bool = False, as_box=False) -> VideoShipper | VideosContainer:
        return super().invoke(iterable=iterable, developerKey=developerKey, 
                              retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
                              max_workers=max_workers, debug=debug, as_box=as_box)