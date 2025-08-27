from ..base import IterableRetriever, PipeSettings
from .pipe import SearchPipe
from .params import SearchParams, SearchTypeCheckboxProps, SearchParamProps


class SearchRetriever(IterableRetriever):
    """
    Retrieve channel, playlist, or video by given keywords.

    Parameters
    ----------
    iterable : list of SearchParamProps
        A list of SearchParamProps.
    developerKey : str
        API key obtained from Google Dev Console.
    types : SearchTypeCheckboxProps
        Specify if channel, video, or playlist will be included in the search.
    settings : PipeSettings
        Determines how many pages of response to be obtained.
    max_workers : int
        Determines maximum concurrent threads in multithreading mode.
    debug : bool
        Print request uri if set as True.
    """

    def __init__(self, iterable: list[SearchParamProps], developerKey: str, 
                 types: SearchTypeCheckboxProps,
                 settings: PipeSettings = PipeSettings(), max_workers=8, debug=False):
        super().__init__(iterable=iterable, developerKey=developerKey, settings=settings, max_workers=max_workers, debug=debug)
        # these parameters need to be overwritten
        self.types = types
        self.pipe = SearchPipe
    
    def _create_params(self, i: SearchParamProps):
        return SearchParams(**i.to_dict(), type=self.types.convert())
    
    def invoke(self, output_folder="backup/SearchRetriever", flatten_result=True,
           filename=None, backup=True, backup_when_halted=False, multithread=False):
        # print("settings inside SearchRetriever:", self.settings)
        return super().invoke(output_folder=output_folder, flatten_result=True, filename=filename, backup=backup, backup_when_halted=backup_when_halted, multithread=multithread)