from dataclasses import dataclass

from src.pipeline.pipe import ChannelPlaylistPipe
from src.pipeline.pipe.base import RetrieveMethod
from src.playlist import PlaylistsResponse
from src.base.utils import flatten_chain


@dataclass
class ChannelPlaylistsWorker:
    def __init__(self, channelId: str, retrieval: RetrieveMethod="head", n=None):
        """
        fetch metadata from ChannelPlaylistPipe and pack to product
        """
        self.responses: dict | list[dict] = ChannelPlaylistPipe(channelId=channelId, 
                                                                      retrieval=retrieval, n=n).run_pipe()
        self.raw_items = [response.get("items") for response in self.responses]
        self.processed_responses: list[PlaylistsResponse] = [PlaylistsResponse(response) for response in self.responses]
        self.playlist_items: list[PlaylistsResponse] = flatten_chain([response.items for response in self.processed_responses])