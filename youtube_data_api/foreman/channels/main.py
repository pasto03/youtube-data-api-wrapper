from youtube_data_api.retriever import ChannelsRetriever
from youtube_data_api.container import ChannelsContainer
from youtube_data_api.shipper import ChannelShipper

from youtube_data_api.foreman.base import UniqueForeman


class ChannelsForeman(UniqueForeman):
    """
    Retrieve channel details given channelId(s) and convert to 1D dict.
    """
    def __init__(self):
        super().__init__()
        self.retriever = ChannelsRetriever
        self.container = ChannelsContainer
        self.shipper = ChannelShipper
        self.name = "channels"

    def _pack(self, raw_items) -> ChannelsContainer:
        return super()._pack(raw_items)
    
    def _ship(self, box, backup=True) -> ChannelShipper:
        return super()._ship(box, backup)

    def invoke(self, iterable: list[str], developerKey: str, backup=True, as_box=False) -> ChannelShipper | ChannelsContainer:
        return super().invoke(iterable=iterable, developerKey=developerKey, backup=backup, as_box=as_box)