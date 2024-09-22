from typing import TypeAlias, Literal
from tqdm import tqdm
import math


from ...utils import flatten_chain
from .params import PlaylistsParams


RetrieveMethod: TypeAlias = Literal["head", "custom", "all"]

class PlaylistsPipe:
    """
    Receive one channelId and return playlist resources
    Only PlaylistsRetriever is supposed to implement this object
    """
    def __init__(self, params: PlaylistsParams, playlists_fn=None, 
                 retrieval: RetrieveMethod = "head", n=10):
        self.params = params
        self.playlists_fn = playlists_fn
        self.retrieval = retrieval
        self.n = n
        self.hard_limit = 50
        
    def _get_response(self, pageToken=None, n=None) -> dict:
        if not self.playlists_fn:
            raise ValueError("Do not implement this object explicitly. Use PlaylistsRetriever instead.")
        
        self.params.pageToken = pageToken
        self.params.maxResults = 50 if not n else n
#         print(self.params)
        request = self.playlists_fn.list(**self.params.to_dict())
        response = request.execute()
        return response
    
    def _get_all_response(self) -> list[dict]:
        # print("inside _get_all_response")
        all_response = list()
        first_response = self._get_response()
        nextPageToken = first_response.get("nextPageToken")
        # print("nextPageToken: {}".format(nextPageToken))
        page_info = first_response['pageInfo']
        num_page = math.ceil(page_info['totalResults'] / page_info['resultsPerPage'])
        if not nextPageToken:
            return [first_response]
        
        all_response.append(first_response)
#         print("num pages:", num_page)
        bar = tqdm(total=num_page, desc="fetching response items...")
        bar.update()   # first batch already obtained
        count = 0
        
        while nextPageToken:
            response = self._get_response(pageToken=nextPageToken)
            all_response.append(response)
            nextPageToken = response.get("nextPageToken")
#             print("Current count:", count)
#             print("nextPageToken: {}".format(nextPageToken))
            bar.update()
            count += 1
        
        all_response = flatten_chain([i["items"] for i in all_response])
        bar.set_description("{} playlistItems obtained.".format(len(all_response)))
        bar.close()
        
        return all_response
    
    def run_pipe(self) -> list[dict] | None:
        """call API and return list of playlists"""
        if self.retrieval == "head":
            return self._get_response().get("items")
        
        elif self.retrieval == "custom":
            n = self.n
            assert n > 0 and type(n) == int, "only positive integer allowed"
            n = min(n, self.hard_limit)
            return self._get_response(n=n).get("items")
        
        elif self.retrieval == "all":
            return self._get_all_response()