from youtube_data_api.retriever import VideosRetriever
from youtube_data_api.container import VideosContainer
from youtube_data_api.shipper import VideoShipper

from youtube_data_api.foreman.base import UniqueForeman


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
    
    def _ship(self, box, backup=True) -> VideoShipper:
        return super()._ship(box, backup)

    def invoke(self, iterable: list[str], developerKey: str, backup=True, as_box=False) -> VideoShipper | VideosContainer:
        return super().invoke(iterable=iterable, developerKey=developerKey, backup=backup, as_box=as_box)