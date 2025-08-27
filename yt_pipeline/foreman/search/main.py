from dataclasses import asdict

from ...retriever import RetrieverSettings, SearchRetriever
from ...container import SearchContainer
from ...shipper import SearchShipper

from ...retriever.base import PipeSettings
from ...retriever.search.params import SearchTypeCheckboxProps, SearchParamProps

from ...foreman.base import IterableForeman


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

    def _retrieve(self, iterable: list[str], developerKey: str,
                pipe_settings: PipeSettings = None, retriever_settings: RetrieverSettings = None, max_workers=8, debug=False
                ) -> list[dict]:
        worker = self.retriever(iterable=iterable, developerKey=developerKey, types=self.types, settings=pipe_settings, 
                                max_workers=max_workers, debug=debug)
        return worker.invoke(**asdict(retriever_settings))

    def _pack(self, raw_items) -> SearchContainer:
        return super()._pack(raw_items)
    
    def _ship(self, box, backup=False) -> SearchShipper:
        return super()._ship(box, backup)

    def invoke(self, iterable: list[SearchParamProps], developerKey: str,
               pipe_settings: PipeSettings,
               retriever_settings = RetrieverSettings(output_folder="backup/SearchRetriever"), 
               backup_shipper=True, max_workers: int = 8, debug: bool = False, as_box=False) -> SearchShipper | SearchContainer:
        return super().invoke(iterable=iterable, developerKey=developerKey, pipe_settings=pipe_settings, 
                              retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
                              max_workers=max_workers, debug=debug, as_box=as_box)