from ...retriever import RetrieverSettings, ChannelsRetriever
from ...container import ChannelsContainer
from ...shipper import ChannelShipper

from ...foreman.base import UniqueForeman


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
    
    def _ship(self, box, backup=False) -> ChannelShipper:
        return super()._ship(box, backup)

    def invoke(self, iterable: list[str], developerKey: str, 
               retriever_settings = RetrieverSettings(output_folder="backup/ChannelsRetriever"), 
               backup_shipper=True, max_workers: int = 8, debug: bool = False, as_box=False) -> ChannelShipper | ChannelsContainer:
        return super().invoke(iterable=iterable, developerKey=developerKey, 
                              retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
                              max_workers=max_workers, debug=debug, as_box=as_box)