from dataclasses import dataclass, asdict
from typing import TypeAlias, Literal

RetrieveMethod: TypeAlias = Literal["head", "custom", "all"]


@dataclass
class PipeSettings:
    """
    Settings for IterablePipe.
    
    Args:
        retrieval (RetrieveMethod): 
            - head: only retrieve n items for first page where n=50
            - custom: only retrieve n items for first page where n=n
            - all: retrieve max_page of items
        n(int): effective when retrieval="custom"
        mx_page(int): no. of pages to retrieve
    """
    retrieval: RetrieveMethod = "all"
    n: int = 50
    max_page: int = 5
        
    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}