from typing import TypeAlias, Literal
import math

from .params import BaseParams


RetrieveMethod: TypeAlias = Literal["head", "custom", "all"]
width = 3   # text format


class IterablePipe:
    """
    Receive params and return resources
    Only Retriever is supposed to implement this object
    """
    def __init__(self, params: BaseParams, pipe_fn=None, 
                 retrieval: RetrieveMethod = "head", n=10):
        self.params = params
        self.pipe_fn = pipe_fn
        self.retrieval = retrieval
        self.n = n   # only valid when retrieval set to "custom"
        self.hard_limit = 50

        # will be assigned a value when _get_all_response() is called
        self._page_info = None
        
    def _get_response(self, pageToken=None, n=None) -> dict:
        if not self.pipe_fn:
            raise ValueError("Do not implement this object explicitly. Use Retriever instead.")
        
        self.params.pageToken = pageToken
        self.params.maxResults = 50 if not n else n
#         print(self.params)
        request = self.pipe_fn.list(**self.params.to_dict())
        response = request.execute()
        return response
    
    def _get_all_response(self, max_page=None) -> list[dict]:
        # print("inside _get_all_response")
        all_response = list()
        first_response = self._get_response()
        # print("First response:", first_response)
        
        nextPageToken = first_response.get("nextPageToken")
        # print("nextPageToken: {}".format(nextPageToken))
        page_info: dict = first_response['pageInfo']
        # print("pageInfo:", page_info)
        # return with empty list when no results obtained
        if not page_info['resultsPerPage']:
            return all_response

        num_page = math.ceil(page_info['totalResults'] / page_info['resultsPerPage'])

        # record API call page info
        self._page_info = page_info

        # specifically for any pipe that needs early stop(eg. SearchPipe)
        if max_page:
            num_page = min(max_page, num_page)
            
        all_response.append(first_response)
        if not nextPageToken:
            return all_response
        
        # all_response.extend(first_response.get("items"))

#         print("num pages:", num_page)
        # bar = tqdm(total=num_page)
        # bar.update()   # first batch already obtained
        count = 1
        # bar.set_description("{:^{}s} / {:^{}s} pages fetched.".format(str(count), width, str(num_page), width))
        
        while nextPageToken and (count <= num_page):
            response = self._get_response(pageToken=nextPageToken)
            # print("new response:", response)
            all_response.append(response)
            nextPageToken = response.get("nextPageToken")
            # print("Current count:", count)
#             print("nextPageToken: {}".format(nextPageToken))
            # bar.update()
            count += 1
        
        # all_response = flatten_chain([i["items"] for i in all_response])
        # bar.set_description("{} items obtained.".format(len(all_response)))
        # bar.close()
        
        return all_response
    
    def run_pipe(self, items_only=True) -> list[dict] | None:
        """call API and return list of items"""
        # print("run_pipe() is called")
        if self.retrieval == "head":
            response = self._get_response()
            return response.get("items") if items_only else response
        
        elif self.retrieval == "custom":
            n = self.n
            assert n > 0 and type(n) == int, "only positive integer allowed"
            n = min(n, self.hard_limit)
            response = self._get_response(n=n)
            return response.get("items") if items_only else response
        
        elif self.retrieval == "all":
            all_response = self._get_all_response()
            # print("response: ", all_response)
            all_items = list()
            for response in all_response:
                all_items.extend(response.get("items"))
            # all_items = [response.get("items") for response in all_response]
            return all_items if items_only else all_response
    

class UniquePipe:
    """
    Receive params and return unique pair of resources
    Only Retriever is supposed to implement this object
    """
    def __init__(self, params: BaseParams, pipe_fn=None):
        self.params = params
        self.pipe_fn = pipe_fn
        
    def _get_response(self, **kwargs) -> dict:
        if not self.pipe_fn:
            raise ValueError("Do not implement this object explicitly. Use Retriever instead.")
            
        request = self.pipe_fn.list(**self.params.to_dict())
        response = request.execute()
        return response
    
    def run_pipe(self, items_only=True) -> list[dict] | None:
        """fetch response from API; if no item fetched, return None"""
        response = self._get_response()
        return response.get("items") if items_only else response