from youtube_data_api.retriever import ChannelsRetriever
from youtube_data_api.container import ChannelsContainer
from youtube_data_api.shipper import ChannelShipper

from youtube_data_api.foreman.base import UniqueForeman


class ChannelsForeman(UniqueForeman):
    """
    Retrieve channel details and convert to 1D dict.
    """
    def __init__(self):
        super().__init__()
        self.retriever = ChannelsRetriever
        self.container = ChannelsContainer
        self.shipper = ChannelShipper

    def invoke(self, iterable: list[str], developerKey: str, backup=True) -> ChannelShipper:
        return super().invoke(iterable=iterable, developerKey=developerKey, backup=backup)