from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class PlaylistItemsCheckboxProps:
    """
    set any property in this checkbox to true for API to return the specific property
    """
    contentDetails: bool = True
    snippet: bool = True
    status: bool = True
        
    def convert(self):
        """convert selected checkbox parts to string"""
        return ",".join([k for k, v in asdict(self).items() if v is True])
    
@dataclass
class PlaylistItemsParams:
    part: str
    playlistId: str
#     id: str
    pageToken: Optional[str] = None
    maxResults: int = 50   
        
    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}