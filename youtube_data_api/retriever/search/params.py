from typing import Optional, TypeAlias, Literal
from dataclasses import dataclass, asdict, field


OrderProps: TypeAlias = Literal["date", "rating", "viewCount", "relevance", "title", "videoCount"]
VideoDurationProps: TypeAlias = Literal["any", "long", "medium", "short"]

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
class SearchParamProps:
    q: str
    channelId: Optional[str] = None

    videoCategoryId: Optional[str] = None
    videoDuration: Optional[VideoDurationProps] = "any"

    order: Optional[OrderProps] = "relevance"
    publishedAfter: Optional[str] = None    # RFC 3339 formatted date-time value

    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}
    

@dataclass
class SearchParams:
    q: str
    type: str 
        
    channelId: Optional[str] = None
    pageToken: Optional[str] = None

    videoCategoryId: Optional[str] = None
    videoDuration: Optional[VideoDurationProps] = "any"

    part: str = "snippet"   # constant
    maxResults: int = 50

    order: OrderProps = "relevance" 
    publishedAfter: Optional[str] = None

    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}
    

