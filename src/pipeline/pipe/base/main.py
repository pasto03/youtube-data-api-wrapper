from tqdm import tqdm
from dataclasses import dataclass, field

from typing import TypeAlias, Literal

RetrieveMethod: TypeAlias = Literal["head", "custom", "all"]
        
        
@dataclass
class BaseFilter:    
    def to_dict(self):
        raise NotImplementedError


@dataclass
class BasePipe:
    retrieval: RetrieveMethod = "head"
    n: int | None = None
    N: int = field(init=False)

    def __post_init__(self):
        self.N = 5
        self.HARD_LIMIT = 50
    
    def _get_response(self, n, pageToken=None) -> dict:
        """overwrite this function when inherited"""
        response = {"pageInfo": {"totalResults": n*3, "resultsPerPage": n}}
        
        return response
    
    def _get_all_response(self) -> list[dict]:
        # print("inside _get_all_response")
        all_response = list()
        first_response = self._get_response(self.HARD_LIMIT)
        nextPageToken = first_response.get("nextPageToken")
        # print("nextPageToken: {}".format(nextPageToken))
        page_info = first_response['pageInfo']
        num_page = page_info['totalResults'] // page_info['resultsPerPage']
        if not nextPageToken:
            return [first_response]
        
        all_response.append(first_response)
        # bar = tqdm(total=num_page, desc="fetching response items...")
        count = 0
        
        while nextPageToken:
            response = self._get_response(n=self.HARD_LIMIT, pageToken=nextPageToken)
            all_response.append(response)
            nextPageToken = response.get("nextPageToken")
            # print("nextPageToken: {}".format(nextPageToken))
            # bar.update()
            count += 1

        # if count < num_page:
            # bar.set_description("Early ended due to API constraint of 500 items.")

        # bar.close()
        
        return all_response
        
    def run_pipe(self) -> list[dict]:
        if self.retrieval == "head":
            return [self._get_response(self.N)]
        
        elif self.retrieval == "custom":
            n = self.n
            assert n > 0 and type(n) == int, "only positive integer allowed"
            n = min(n, self.HARD_LIMIT)
            return [self._get_response(n)]
        
        elif self.retrieval == "all":
            return self._get_all_response()