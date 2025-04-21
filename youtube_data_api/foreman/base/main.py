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
        self.name = "unique"

    def _retrieve(self, iterable: list[str], developerKey: str, backup=True) -> list[dict]:
        worker = self.retriever(iterable=iterable, developerKey=developerKey)
        return worker.invoke(backup=backup)
    
    def _pack(self, raw_items: list[dict]) -> BaseContainer:
        return self.container(raw_items)
    
    def _ship(self, box: BaseContainer, backup=True) -> BaseShipper:
        shipper = self.shipper()
        shipper.invoke(box.items, backup=backup)
        return shipper

    def invoke(self, iterable: list[str], developerKey: str, backup=True, as_box=False) -> BaseShipper | BaseContainer:
        # 1. retrieve raw items
        raw_items = self._retrieve(iterable, developerKey=developerKey, backup=backup)

        # 2. box raw items
        box = self._pack(raw_items)

        if as_box:
            return box

        # 3. pack boxes
        shipper = self._ship(box, backup=backup)
        return shipper
    

class IterableForeman:
    """
    Base foreman class for PlaylistItems, Playlists
    """
    def __init__(self):
        self.retriever = IterableRetriever
        self.container = BaseContainer
        self.shipper = BaseShipper
        self.name = "iterable"

    def _retrieve(self, iterable: list[str], developerKey: str, settings: PipeSettings, backup=True) -> list[dict]:
        worker = self.retriever(iterable=iterable, developerKey=developerKey, settings=settings)
        return worker.invoke(backup=backup)
    
    def _pack(self, raw_items: list[dict]) -> BaseContainer:
        return self.container(raw_items)
    
    def _ship(self, box: BaseContainer, backup=True) -> BaseShipper:
        shipper = self.shipper()
        shipper.invoke(box.items, backup=backup)
        return shipper

    def invoke(self, iterable: list[str], developerKey: str, 
               settings: PipeSettings = PipeSettings(), backup=True, as_box=False) -> BaseShipper | BaseContainer:
        # 1. retrieve raw items
        raw_items = self._retrieve(iterable, developerKey=developerKey, settings=settings, backup=backup)

        # 2. box raw items
        box = self._pack(raw_items)

        if as_box:
            return box

        # 3. pack boxes
        shipper = self._ship(box, backup=backup)
        return shipper