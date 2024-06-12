from dataclasses import dataclass
from typing import Optional

from utils import search_fn

from src.search.props import OrderProps, QueryTypeProps
from src.search.params import SearchParams
from src.pipeline.pipe.base import BasePipe


@dataclass
class SearchPipe(BasePipe):
    """return list of items by query and(or) channelId filter"""
    q: str = None
    channelId: Optional[str] = None
    order: OrderProps = "relevance"
    type: QueryTypeProps = "video"
    
    def _get_response(self, n: int, pageToken=None) -> dict:
        params = SearchParams(
            q=self.q,
            channelId=self.channelId,
            part="snippet", 
            pageToken=pageToken,
            maxResults=n,
            order=self.order,
            type=self.type
        )

        request = search_fn.list(**params.to_dict())
        response = request.execute()
        return response