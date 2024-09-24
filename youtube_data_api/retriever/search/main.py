from ..base import IterableRetriever, PipeSettings
from .pipe import SearchPipe
from .params import SearchParams, SearchTypeCheckboxProps


class SearchRetriever(IterableRetriever):
    def __init__(self, keywords: list[str], developerKey: str, 
                 types: SearchTypeCheckboxProps = SearchTypeCheckboxProps(),
                 settings: PipeSettings = PipeSettings()):
        super().__init__(iterable=keywords, developerKey=developerKey, settings=settings)
        # these parameters need to be overwritten
        self.types = types
        self.pipe_fn = self.client.search()
        self.pipe = SearchPipe
    
    def _create_params(self, i):
        return SearchParams(q=i, type=self.types.convert(), order="relevance")
    
    def invoke(self, output_folder="backup/SearchRetriever", 
           filename=None, backup=True) -> list[dict]:
        return super().invoke(output_folder=output_folder, filename=filename, backup=backup)