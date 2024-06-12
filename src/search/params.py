from typing import Optional
from dataclasses import dataclass, asdict, field
from src.search.props import OrderProps, QueryTypeProps

@dataclass
class SearchParams:
    q: str
    
    channelId: Optional[str] = None
    location: Optional[str] = None
    locationRadius: Optional[str] = None
    publishedAfter: Optional[str] = None
    publishedBefore: Optional[str] = None
    pageToken: Optional[str] = None

    part: str = "snippet"
    maxResults: int = 5
    order: OrderProps = "relevance" 
    type: QueryTypeProps = "video"  
    
    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}