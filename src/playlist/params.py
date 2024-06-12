from typing import Optional
from dataclasses import dataclass, asdict

from ..base.params import BaseParams


@dataclass
class PlaylistsFilter:
    channelId: Optional[str] = None
    id: Optional[str] = None
    mine: Optional[bool] = None
        
    def __post_init__(self):
        filters = [self.channelId, self.id, self.mine]
        if not sum([i is not None for i in filters]) == 1:
            raise ValueError("specify exactly one of the following parameters")
    
    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}

@dataclass
class PlaylistsParams(BaseParams):
    part: str
    filter: PlaylistsFilter
    pageToken: str = None
    maxResults: int = 5
        
    def __post_init__(self):
        self.filter = self.filter.to_dict()
        
    def to_dict(self):
        params = dict()
        for (k, v) in asdict(self).items():
            if v is not None:
                if k == "filter":
                    params.update(v)
                else:
                    params.update({k:v})
        return params