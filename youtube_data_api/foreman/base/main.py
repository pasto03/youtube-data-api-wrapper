from youtube_data_api.retriever.base import UniqueRetriever, IterableRetriever
from youtube_data_api.container.base import BaseContainer
from youtube_data_api.shipper.base import BaseShipper


from youtube_data_api.retriever.base import PipeSettings


class UniqueForeman:
    """
    Base foreman class for Channels and Videos
    """
    def __init__(self):
        self.retriever = UniqueRetriever
        self.container = BaseContainer
        self.shipper = BaseShipper

    def invoke(self, iterable: list[str], developerKey: str, backup=True) -> BaseShipper:
        # 1. retrieve raw items
        worker = self.retriever(iterable=iterable, developerKey=developerKey)
        raw_items = worker.invoke(backup=backup)

        # 2. box raw items
        box = self.container(raw_items)

        # 3. pack boxes
        shipper = self.shipper()
        shipper.invoke(box.items, backup=backup)
        return shipper
    

class IterableForeman:
    """
    Base foreman class for PlaylistItems, Playlists
    """
    def __init__(self):
        self.retriever = IterableRetriever
        self.container = BaseContainer
        self.shipper = BaseShipper

    def invoke(self, iterable: list[str], developerKey: str, 
               settings: PipeSettings = PipeSettings, backup=True) -> BaseShipper:
        # 1. retrieve raw items
        worker = self.retriever(iterable=iterable, developerKey=developerKey, settings=settings)
        raw_items = worker.invoke(backup=backup)

        # 2. box raw items
        box = self.container(raw_items)

        # 3. pack boxes
        shipper = self.shipper()
        shipper.invoke(box.items, backup=backup)
        return shipper