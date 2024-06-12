from src.search.props import QueryTypeProps, OrderProps, RetrieveMethod
from src.search.channel import SearchChannelItem, SearchChannelResponse
from src.search.video import SearchVideoItem, SearchVideoResponse
from src.search.playlist import SearchPlaylistItem, SearchPlaylistResponse
from src.pipeline.pipe import SearchPipe

from dataclasses import dataclass
from typing import Optional, Dict

from src.base.utils import flatten_chain


@dataclass
class SearchWorker:
    """this worker process user search request, fetch metadata from API, then parse metadata to object"""
    responses: list[dict]
    raw_items: list[dict | None]
    processed_responses: list[SearchChannelResponse | SearchPlaylistResponse | SearchVideoResponse]
    search_items: list[SearchChannelItem | SearchPlaylistItem | SearchVideoItem]

    def __init__(self, q: str, channelId: Optional[str]=None, retrieval: RetrieveMethod = "head", n=None,
                 order: OrderProps = "relevance", type: QueryTypeProps = "video"):
        self.responses = SearchPipe(retrieval=retrieval, n=n, q=q, channelId=channelId, 
                                    order=order, type=type).run_pipe()
        self._parser_map: Dict[QueryTypeProps, SearchChannelResponse | SearchPlaylistResponse | SearchVideoResponse] = {
            "channel": SearchChannelResponse, 
            "playlist": SearchPlaylistResponse,
            "video": SearchVideoResponse
        }
        self._parser = self._parser_map[type]
        self.raw_items = [response.get("items") for response in self.responses]
        self.processed_responses = [self._parser(response) for response in self.responses]
        self.search_items = flatten_chain([response.items for response in self.processed_responses])