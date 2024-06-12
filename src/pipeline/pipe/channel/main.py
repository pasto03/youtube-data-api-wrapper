from dataclasses import dataclass, field
from typing import Optional, Literal

from utils import channel_fn

from src.channel.props import ChannelCheckboxProps
from src.channel.params import ChannelParams
from src.pipeline.pipe.base import BasePipe


@dataclass
class ChannelPipe(BasePipe):
    """
    obtain channel details in json of an unique channelId
    """
    retrieval: Literal["unique"] = field(init=False)
    n: int = field(init=False)
    channelId: str = None
    partProps: ChannelCheckboxProps = ChannelCheckboxProps(snippet=True, statistics=True)

    def __post_init__(self):
        super().__post_init__()
        self.retrieval = "unique"
        self.n = 1
    
    def _get_response(self, n: int, pageToken=None) -> dict:
        if not self.channelId:
            raise ValueError("The 'channelId' parameter cannot be empty")
        params = ChannelParams(
            part=self.partProps.convert(),
            id=self.channelId,
            pageToken=pageToken,
            maxResults=n
        )

        request = channel_fn.list(**params.to_dict())
        response = request.execute()
        return response
    
    def _get_all_response(self, **kwargs):
        raise NotImplementedError
    
    def run_pipe(self) -> list[dict] | None:
        """fetch response from API; if no item fetched, return None"""
        response = self._get_response(n=1)
        if not response.get("items"):
            return None
        return [response]