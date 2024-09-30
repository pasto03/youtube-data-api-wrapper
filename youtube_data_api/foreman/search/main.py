from youtube_data_api.retriever import SearchRetriever
from youtube_data_api.container import SearchContainer
from youtube_data_api.shipper import SearchShipper

from youtube_data_api.retriever.base import PipeSettings
from youtube_data_api.retriever.search.params import SearchTypeCheckboxProps, SearchParamProps


class SearchForeman:
    """
    Retrieve search details and convert to 1D dict.
    """
    def __init__(self) -> None:
        pass

    def invoke(self, iterable: list[SearchParamProps], developerKey: str, 
               types: SearchTypeCheckboxProps = SearchTypeCheckboxProps(),
               settings: PipeSettings = PipeSettings, backup=True) -> SearchShipper:
        # 1. retrieve raw items
        worker = SearchRetriever(iterable=iterable, developerKey=developerKey, types=types, settings=settings)
        raw_items = worker.invoke(backup=backup)

        # 2. box raw items
        box = SearchContainer(raw_items)

        # 3. pack boxes
        shipper = SearchShipper()
        shipper.invoke(box.items, backup=backup)
        return shipper