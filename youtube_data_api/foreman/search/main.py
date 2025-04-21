from youtube_data_api.retriever import SearchRetriever
from youtube_data_api.container import SearchContainer
from youtube_data_api.shipper import SearchShipper

from youtube_data_api.retriever.base import PipeSettings
from youtube_data_api.retriever.search.params import SearchTypeCheckboxProps, SearchParamProps

from youtube_data_api.foreman.base import IterableForeman


class SearchForeman(IterableForeman):
    """
    Retrieve search details given a list of SearchParamProps and convert to 1D dict.
    """
    def __init__(self, types: SearchTypeCheckboxProps):
        super().__init__()
        self.retriever = SearchRetriever
        self.container = SearchContainer
        self.shipper = SearchShipper
        self.name = "search"

        self.types = types

    def _retrieve(self, iterable, developerKey, settings, backup=True) -> list[dict]:
        worker = self.retriever(iterable=iterable, developerKey=developerKey, types=self.types, settings=settings)
        return worker.invoke(backup=backup)

    def _pack(self, raw_items) -> SearchContainer:
        return super()._pack(raw_items)
    
    def _ship(self, box, backup=True) -> SearchShipper:
        return super()._ship(box, backup)

    def invoke(self, iterable, developerKey, settings: PipeSettings = PipeSettings(), backup=True, as_box=False) -> SearchShipper | SearchContainer:
        return super().invoke(iterable, developerKey=developerKey, settings=settings, backup=backup, as_box=as_box)