from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class VideoCategoriesParams:
    # only specify one of the following parameters
    id: Optional[str] = None
    regionCode: Optional[str] = None

    part: str = "snippet"
    hl: str = "en_US"

    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}