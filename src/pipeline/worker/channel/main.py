from dataclasses import dataclass

from src.pipeline.pipe import ChannelPipe
from src.channel import ChannelItem, ChannelResponse
from src.base.utils import flatten_chain


@dataclass
class ChannelWorker:
    channelId: str
    responses: list[dict] | None = None
    raw_items: list | None = None
    processed_responses: list[ChannelResponse] | None = None
    channel_items: list[ChannelItem] | None = None

    def __init__(self, channelId: str):
        self.channelId = channelId
        self.responses: list[dict] | None = ChannelPipe(channelId=channelId).run_pipe()
        if self.responses:
            self.raw_items = [response.get("items") for response in self.responses]
            self.processed_responses: list[ChannelResponse] = [ChannelResponse(response) for response in self.responses]
            self.channel_items: list[ChannelItem] = flatten_chain([response.items for response in self.processed_responses])