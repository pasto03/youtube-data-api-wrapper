from typing import Optional, TypeAlias, Literal
from dataclasses import dataclass, asdict, field


OrderProps: TypeAlias = Literal["date", "rating", "viewCount", "relevance", "title", "videoCount"]

@dataclass
class SearchTypeCheckboxProps:
    """
    set any property in this checkbox to true for API to return the specific property
    """
    channel: bool = True
    playlist: bool = True
    video: bool = True
        
    def convert(self):
        """convert selected checkbox parts to string"""
        return ",".join([k for k, v in asdict(self).items() if v is True])

    
@dataclass
class SearchParams:
    q: str
    type: str 
        
    channelId: Optional[str] = None
    pageToken: Optional[str] = None

    part: str = "snippet"   # constant
    maxResults: int = 50
    order: OrderProps = "relevance" 

    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}