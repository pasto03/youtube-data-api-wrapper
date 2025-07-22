from dataclasses import asdict

from ...retriever.base import UniqueRetriever, IterableRetriever, BaseRetriever, PipeSettings, RetrieverSettings
from ...container.base import BaseContainer
from ...container import HttpErrorContainer
from ...shipper.base import BaseShipper
from ...retriever import SearchParamProps


class BaseForeman:
    """
    Base foreman class
    """
    def __init__(self):
        self.retriever = BaseRetriever
        self.container = BaseContainer
        self.shipper = BaseShipper
        self.name = "base"

        # save errors returned from retriever
        self.errors: list[HttpErrorContainer | Exception] = list()

        # save ignored errors
        self.ignored_errors: list[HttpErrorContainer] = list()

    def _retrieve(self, iterable: list[str], developerKey: str,
                pipe_settings: PipeSettings = None, retriever_settings: RetrieverSettings = None, max_workers=8, debug=False):
        if pipe_settings:
            worker: IterableRetriever = self.retriever(iterable=iterable, developerKey=developerKey, settings=pipe_settings, max_workers=max_workers, debug=debug)
        else:
            worker: UniqueRetriever | BaseRetriever = self.retriever(iterable=iterable, developerKey=developerKey, max_workers=max_workers, debug=debug)

        self.ignored_errors = worker.ignored_errors
        return worker.invoke(**asdict(retriever_settings))
    
    def _pack(self, raw_items: list[dict]) -> BaseContainer:
        return self.container(raw_items)
    
    def _ship(self, box: BaseContainer, backup=True) -> BaseShipper:
        shipper = self.shipper()
        shipper.invoke(box.items, backup=backup)
        return shipper

    def invoke(self, iterable: list[str], developerKey: str, 
                pipe_settings: PipeSettings = None, 
                retriever_settings: RetrieverSettings = RetrieverSettings(output_folder="backup/BaseRetriever"),
                backup_shipper=True, max_workers=8, debug=False,
                as_box=False) -> BaseShipper | BaseContainer:
        # 1. retrieve results
        results = self._retrieve(iterable, developerKey=developerKey, pipe_settings=pipe_settings, retriever_settings=retriever_settings, max_workers=max_workers, debug=debug)

        # 1.2 handle different results
        if isinstance(results, tuple):
            raw_items, error = results
            self.errors.append(error)
        else:
            raw_items = results

        # 2. box raw items
        box = self._pack(raw_items)

        if as_box:
            return box

        # 3. pack boxes
        shipper = self._ship(box, backup=backup_shipper)
        return shipper


class UniqueForeman(BaseForeman):
    """
    Base foreman class for batch retrievers
    """
    def __init__(self):
        self.retriever = UniqueRetriever
        self.name = "unique"

    def invoke(self, iterable: list[str], developerKey: str, 
               retriever_settings = RetrieverSettings(output_folder="backup/UniqueRetriever"), 
               backup_shipper=True, max_workers: int = 8, debug: bool = False, as_box=False):
        return super().invoke(iterable, developerKey=developerKey, pipe_settings=None, 
                              retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
                              max_workers=max_workers, debug=debug, as_box=as_box)


class IterableForeman(BaseForeman):
    """
    Base foreman class for iterable retrievers
    """
    def __init__(self):
        self.retriever = IterableRetriever
        self.name = "iterable"

    def invoke(self, iterable: list[str] | list[SearchParamProps], developerKey: str,
               pipe_settings: PipeSettings,
               retriever_settings = RetrieverSettings(output_folder="backup/UniqueRetriever"), 
               backup_shipper=True, max_workers: int = 8, debug: bool = False, as_box=False):
        return super().invoke(iterable=iterable, developerKey=developerKey, pipe_settings=pipe_settings, 
                              retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
                              max_workers=max_workers, debug=debug, as_box=as_box)