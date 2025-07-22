from googleapiclient.errors import HttpError

from ..base import SingleRetriever, BaseRetriever
from .pipe import CaptionsPipe
from .params import CaptionsParams

from ...utils import handle_backup
from ...container import HttpErrorContainer


# class CaptionsRetriever:
#     """
#     Retrieve caption resource from given videoId

#     Parameters
#     ----------
#     params : list[CaptionsParams]
#         list of CaptionsParams object as parameter.
#     developerKey : str
#         API key obtained from Google Dev Console.
#     """
#     def __init__(self, params: list[CaptionsParams], developerKey: str):
#         self.pipe = CaptionsPipe

#         self.params = params
#         self.developerKey = developerKey

#     def _create_pipes(self):
#         return [
#                 self.pipe(params=i, developerKey=self.developerKey)
#                 for i in self.params if i
#             ]
        
#     def invoke(self, output_folder="backup/CaptionsRetriever", 
#                filename=None, backup=True) -> list[dict] | HttpErrorContainer | Exception:
#         pipe = self._create_pipe()
        
#         try:
#             raw_items = pipe.run_pipe()
#         except Exception as e:
#             if isinstance(e, (HttpError, )):
#                 return HttpErrorContainer.from_http_error(e)
#             else:
#                 return e
        
#         if backup:
#             handle_backup(raw_items, output_folder=output_folder, filename=filename)
        
#         return raw_items

#     def invoke(self, output_folder="backup/CaptionsRetriever", 
#             filename=None, backup=True) -> list[dict]:
#         return super().invoke(output_folder=output_folder, filename=filename, backup=backup)
    

class CaptionsRetriever(BaseRetriever):
    """
    Retrieve caption resource from given videoId

    Parameters
    ----------
    params : list[str]
        list of videoId as parameter.
    developerKey : str
        API key obtained from Google Dev Console.
    """
    def __init__(self, iterable: list[str], developerKey: str, max_workers=8, debug=False):
        super().__init__(iterable=iterable, developerKey=developerKey, max_workers=max_workers, debug=debug)
        self.pipe = CaptionsPipe

    def _create_pipes(self):
        return [
                self.pipe(params=CaptionsParams(videoId=videoId), developerKey=self.developerKey, debug=self.debug)
                for videoId in self.iterable if videoId
            ]
    
    def invoke(self, output_folder="backup/CaptionsRetriever", flatten_result=True, filename=None, backup=True, backup_when_halted=False, multithread=False):
        return super().invoke(output_folder=output_folder, flatten_result=flatten_result, filename=filename, backup=backup, backup_when_halted=backup_when_halted, multithread=multithread)