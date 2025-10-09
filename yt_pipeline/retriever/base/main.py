from dataclasses import dataclass
from googleapiclient.errors import HttpError

from ...utils import split_list, build_client, handle_backup
from .settings import PipeSettings
from .pipe import IterablePipe, UniquePipe
from .params import BaseParams
from .process import multithreading_run_pipe, iterating_run_pipe
from ...container import HttpErrorContainer


@dataclass
class RetrieverSettings:
    """
    settings for retriever execution
    """
    output_folder: str = "backup/UniqueRetriever"
    flatten_result: bool = True
    filename: str | None = None
    backup: bool = False
    backup_when_halted: bool = False
    multithread: bool = False


class BaseRetriever:
    """
    Base retriever class
    """
    def __init__(self, iterable: list[str], developerKey: str, max_workers=8, debug=False):
        self.iterable = iterable
        # self.client = build_client(developerKey)
        # self.pipe_fn = None    # assign by child class
        self.developerKey = developerKey
        self.pipe = IterablePipe | UniquePipe

        self.max_workers = max_workers
        self.debug = debug

        # save ignored errors
        self.ignored_errors: list[HttpErrorContainer] = list()
        
    def _create_params(self, i):
        return BaseParams(part='snippet')
    
    def _create_pipes(self):
        return [
                self.pipe(self._create_params(i), developerKey=self.developerKey)
                for i in self.iterable if i
            ]
    
    def _post_retrieval(self, results: list[dict] | list[list[dict]] | tuple[list[dict] | list[list[dict]], HttpErrorContainer | Exception], output_folder, filename=None, backup=True):
        """
        process results from executed pipes
        - backup
        - results handling
        """
        error = None
        if isinstance(results, list):
            raw_items = results
        else:
            raw_items, error = results

        if backup:
            handle_backup(raw_items, output_folder=output_folder, filename=filename)

        if not error:
            return raw_items
        else:
            return raw_items, error
    
    def invoke(self, output_folder="backup/BaseRetriever", flatten_result=True,
               filename=None, backup=True, backup_when_halted=False, multithread=False
               ) -> list[dict] | list[list[dict]] | tuple[list[dict] | list[list[dict]], HttpErrorContainer | Exception]:
        
        pipes = self._create_pipes()

        # multithread mode
        if multithread:            
            results = multithreading_run_pipe(
                pipes=pipes, ignored_errors=self.ignored_errors, 
                max_workers=self.max_workers, flatten_result=flatten_result,
                output_folder=output_folder, filename=filename, backup_when_halted=backup_when_halted
                )

        # single thread mode
        else:
            results = iterating_run_pipe(
                pipes, ignored_errors=self.ignored_errors, flatten_result=flatten_result, 
                output_folder=output_folder, filename=filename, backup_when_halted=backup_when_halted
                )
            
        return self._post_retrieval(results, output_folder=output_folder, filename=filename, backup=backup)
    

class IterableRetriever(BaseRetriever):
    """
    - one-to-many retrieval; eg. one channelId to multiple playlists
    - one API call per query parameter in iterative; eg. one channelId for one playlist API call
    - one pipe created per query parameter
    """
    def __init__(self, iterable: list[str], developerKey: str, settings=PipeSettings(), max_workers=8, debug=False):
        super().__init__(iterable=iterable, developerKey=developerKey, max_workers=max_workers, debug=debug)
        self.pipe = IterablePipe
        self.settings = settings

    def _create_pipes(self):
        return [
                self.pipe(self._create_params(i), developerKey=self.developerKey, settings=self.settings, debug=self.debug)
                for i in self.iterable if i
            ]
    
    def invoke(self, output_folder="backup/IterableRetriever", flatten_result=True, filename=None, backup=True, backup_when_halted=False, multithread=False):
        return super().invoke(output_folder=output_folder, flatten_result=flatten_result, filename=filename, backup=backup, backup_when_halted=backup_when_halted, multithread=multithread)
    

class UniqueRetriever(BaseRetriever):
    """
    - one-to-one retrieval with batch; eg. one channelId to one channel details, batched channelId to batched channel details
    - batch processing for maximizing API call efficiency
    """
    def __init__(self, iterable: list[str], developerKey: str, max_workers=8, debug=False):
        super().__init__(iterable=iterable, developerKey=developerKey, max_workers=max_workers, debug=debug)
        self.pipe = UniquePipe

        self.chunk_size = 50   # maximum allowed id length in a comma list
        self.chunks = split_list(self.iterable, chunk_size=self.chunk_size)   # split to chunks containing multiple ids
    
    def _create_params(self, chunk: list[str]):
        chunk = ",".join(chunk)
        return BaseParams(part='snippet')
    
    def _create_pipes(self):
        return [
                self.pipe(self._create_params(chunk), developerKey=self.developerKey, debug=self.debug)
                for chunk in self.chunks if chunk
            ]
    
    def invoke(self, output_folder="backup/UniqueRetriever", flatten_result=True, filename=None, backup=True, backup_when_halted=False, multithread=False):
        return super().invoke(output_folder=output_folder, flatten_result=flatten_result, filename=filename, backup=backup, backup_when_halted=backup_when_halted, multithread=multithread)


class SingleRetriever:
    """
    - one-to-one retrieval where only one(group of) item(s) retrieved
    - eg. one caption resource obtained for one videoId
    """
    def __init__(self, params: BaseParams, developerKey: str):
        self.params = params
        # self.client = build_client(developerKey)
        # self.pipe_fn = None
        self.pipe = UniquePipe
        self.developerKey = developerKey

    def _create_pipe(self):
        return self.pipe(params=self.params, developerKey=self.developerKey)
        
    def invoke(self, output_folder="backup/SingleRetriever", 
               filename=None, backup=True) -> list[dict] | HttpErrorContainer | Exception:
        pipe = self._create_pipe()
        
        try:
            raw_items = pipe.run_pipe()
        except Exception as e:
            if isinstance(e, (HttpError, )):
                return HttpErrorContainer.from_http_error(e)
            else:
                return e
        
        if backup:
            handle_backup(raw_items, output_folder=output_folder, filename=filename)
        
        return raw_items