from youtube_data_api.retriever import ChannelsRetriever
from youtube_data_api.container import ChannelsContainer
from youtube_data_api.shipper import ChannelShipper

from youtube_data_api.foreman.base import UniqueForeman


class ChannelsForeman(UniqueForeman):
    def __init__(self):
        super().__init__()
        self.retriever = ChannelsRetriever
        self.container = ChannelsContainer
        self.shipper = ChannelShipper