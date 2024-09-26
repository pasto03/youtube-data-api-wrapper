from youtube_data_api.retriever import VideosRetriever
from youtube_data_api.container import VideosContainer
from youtube_data_api.shipper import VideoShipper

from youtube_data_api.foreman.base import UniqueForeman


class VideosForeman(UniqueForeman):
    """
    Retrieve video details and convert to 1D dict.
    """
    def __init__(self):
        super().__init__()
        self.retriever = VideosRetriever
        self.container = VideosContainer
        self.shipper = VideoShipper

    def invoke(self, iterable: list[str], developerKey: str, backup=True) -> VideoShipper:
        return super().invoke(iterable=iterable, developerKey=developerKey, backup=backup)