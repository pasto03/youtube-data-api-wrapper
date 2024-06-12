from dataclasses import dataclass, asdict

from ..base.params import BaseParams


@dataclass
class ChannelParams(BaseParams):
    part: str
    id: str
    pageToken: str = None
    maxResults: int = 5