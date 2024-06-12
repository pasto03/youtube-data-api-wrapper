from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ChannelCheckboxProps:
    """
    set any property in this checkbox to true for API to return the specific property
    """
    # auditDetails: bool = False
    # brandingSettings: bool = False
    # contentDetails: bool = False
    # contentOwnerDetails: bool = False
    # id: bool = False
    # localizations: bool = False
    snippet: bool = True
    statistics: bool = True
    # status: bool = True
    # topicDetails: bool = False
        
    def convert(self):
        """convert selected checkbox parts to string"""
        return ",".join([k for k, v in asdict(self).items() if v is True])
    

@dataclass
class ChannelParams:
    part: str
    id: str   # id(s)
    pageToken: Optional[str] = None
    maxResults: int = 5    
        
    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}