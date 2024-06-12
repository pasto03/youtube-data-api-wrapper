from dataclasses import dataclass
from typing import Annotated

from src.pipeline.pipe.base import RetrieveMethod
from src.pipeline.pipe import PlaylistItemsPipe
from src.playlist_items import PlaylistItemsResponse, PlaylistItemsItem

from src.base.utils import flatten_chain


@dataclass
class PlaylistItemsWorker:
    def __init__(self, playlistId: str, retrieval:RetrieveMethod="head", n=None):
        """
        fetch metadata from PlaylistItemsPipe and pack to product
        """
        self.playlistId = playlistId
        self.responses: list[dict] = PlaylistItemsPipe(retrieval=retrieval, n=n, playlistId=playlistId).run_pipe()
        self.raw_items = [response.get("items") for response in self.responses]
        self.processed_responses: list[PlaylistItemsResponse] = [PlaylistItemsResponse(response) for response in self.responses]
        self.playlist_items: list[PlaylistItemsItem] = flatten_chain([response.items for response in self.processed_responses])