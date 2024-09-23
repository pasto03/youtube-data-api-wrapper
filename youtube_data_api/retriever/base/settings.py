from dataclasses import dataclass, asdict
from typing import TypeAlias, Literal

RetrieveMethod: TypeAlias = Literal["head", "custom", "all"]


@dataclass
class PipeSettings:
    retrieval: RetrieveMethod = "all"
    n: int = 50
        
    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}