from dataclasses import dataclass, asdict


@dataclass
class BaseCheckboxProps:
    """
    set any property in this checkbox to true for API to return the specific property
    """
    
    def convert(self):
        """convert selected checkbox parts to string"""
        return ",".join([k for k, v in asdict(self).items() if v is True])
    

@dataclass
class OrderProps:
    date: str = "date"
    rating: str = "rating"
    viewCount: str = "viewCount"
    relevance: str = "relevance"
    title: str = "title"
    videoCount: str = "videoCount"