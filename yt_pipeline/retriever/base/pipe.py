import math
from googleapiclient.http import HttpRequest

from ...utils import build_client
from .params import BaseParams
from .settings import PipeSettings


# RetrieveMethod: TypeAlias = Literal["head", "custom", "all"]
width = 3   # text format


class IterablePipe:
    """
    Receive params and return paged resources, eg. one keyword for multiple result items
    """
    def __init__(self, params: BaseParams, developerKey: str, settings: PipeSettings = PipeSettings(), debug=False):
        self.params = params
        self.developerKey = developerKey
        self.client = build_client(developerKey)
        self.pipe_fn = None   # assign by child class
        self.retrieval = settings.retrieval
        self.n = settings.n   # only effective when retrieval set to "custom"
        self.max_page = settings.max_page

        # print("settings received upon initialization:", settings)
        self.settings = settings

        # limit of maxResults
        self.hard_limit = 50

        self.debug = debug
        
        # will be assigned a value when _get_all_response() is called
        self._page_info = None
        
    def _get_response(self, pageToken=None, n=None) -> dict:
        if not self.pipe_fn:
            raise ValueError("Do not implement this object explicitly. Use Retriever instead.")
        
        self.params.pageToken = pageToken
        self.params.maxResults = self.hard_limit if not n else n

        # print("Params inside _get_response(): {}".format(self.params))

        request: HttpRequest = self.pipe_fn.list(**self.params.to_dict())
        if self.debug:
            print("request uri:", request.uri)
        response = request.execute()
        return response
    
    def _get_all_response(self, infinite_query: bool = False) -> list[dict]:
        all_response = list()
        first_response = self._get_response()
        
        nextPageToken = first_response.get("nextPageToken")
        page_info: dict = first_response['pageInfo']

        # return with empty list when no results obtained
        if not page_info['resultsPerPage']:
            return all_response

        num_page = math.ceil(page_info['totalResults'] / page_info['resultsPerPage'])

        # record API call page info
        self._page_info = page_info

        # comment threads only show "resultsPerPage" == "totalResults" even there are more comment threads, so "infinite_query" is to indicate its characteristics
        if infinite_query:
            num_page = self.max_page
        else:
            num_page = min(self.max_page, num_page)
            
        all_response.append(first_response)
        if not nextPageToken:
            return all_response
    
        count = 1
        
        while nextPageToken and (count < num_page):
            response = self._get_response(pageToken=nextPageToken)
            all_response.append(response)

            nextPageToken = response.get("nextPageToken")
            count += 1
        
        return all_response
    
    def run_pipe(self, items_only=True) -> list[dict] | None:
        """call API and return list of items"""
        # print("settings inside run_pipe():", self.settings)
        if self.retrieval == "head":
            response = self._get_response()
            return response.get("items") if items_only else response
        
        elif self.retrieval == "custom":
            n = self.n
            assert n > 0 and type(n) == int, "only positive integer allowed"
            n = min(n, self.hard_limit)
            # print("inside custom retrieval")
            response = self._get_response(n=n)
            return response.get("items") if items_only else response
        
        elif self.retrieval == "all":
            all_response = self._get_all_response()
            # print("response: ", all_response)
            all_items = list()
            for response in all_response:
                all_items.extend(response.get("items"))
            return all_items if items_only else all_response
        
        raise ValueError(f"Invalid retrieval: '{self.retrieval}'. Expected one of 'head', 'custom', or 'all'.")
    

class UniquePipe:
    """
    Receive params and return unique pair of resources, eg. one videoId for one video details
    """
    def __init__(self, params: BaseParams, developerKey: str, debug=False):
        self.params = params
        self.developerKey = developerKey
        self.client = build_client(developerKey)
        self.pipe_fn = None   # assign by child class

        self.debug = debug
        
    def _get_response(self, **kwargs) -> dict:
        if not self.pipe_fn:
            raise ValueError("Do not implement this object explicitly. Use Retriever instead.")
            
        request = self.pipe_fn.list(**self.params.to_dict())

        if self.debug:
            print("request uri:", request.uri)
            
        response = request.execute()
        return response
    
    def run_pipe(self, items_only=True) -> list[dict] | None:
        """fetch response from API; if no item fetched, return None"""
        # print("running pipe")
        response = self._get_response()
        # print("response:", response)
        return response.get("items") if items_only else response