from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class BaseCheckboxProps:
    """
    set any property in this checkbox to true for API to return the specific property
    """
    snippet: bool = True
        
    def convert(self):
        """convert selected checkbox parts to string"""
        return ",".join([k for k, v in asdict(self).items() if v is True])
    

@dataclass
class BaseParams:
    part: str
    pageToken: Optional[str] = None
    maxResults: int = 50   
        
    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}