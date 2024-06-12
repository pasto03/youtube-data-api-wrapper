from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemThumbnail:
    quality: str = None
    url: str = None
    width: Optional[str] = None
    height: Optional[str] = None