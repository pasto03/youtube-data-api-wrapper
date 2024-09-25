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
            - all: retrieve 5 pages of items(capped to avoid quota overuse)
        n(int): effective when retrieval="custom"
    """
    retrieval: RetrieveMethod = "all"
    n: int = 50
        
    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}