from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemThumbnail:
    quality: str = None
    url: str = None
    width: Optional[str] = None
    height: Optional[str] = None


class BaseItem:...


class BaseContainer:
    """
    base items parser class
    
    set self.items = self._extract_item(self.raw_items) when inherited
    """
    def __init__(self, raw_items: list[dict]):
        self.raw_items: raw_items
        
    def _extract_item(self, raw_items):
        raise NotImplementedError
    
    # we assume this function is universal across APIs
    def _extract_thumbnail(self, raw_thumbnails) -> list | list[ItemThumbnail]:
        if len(raw_thumbnails) == 0:
            return list()
        
        thumbnails = []
        thumbnail_items = raw_thumbnails.items()
        
        for (quality, details) in thumbnail_items:
            thumb = ItemThumbnail()
            thumb.quality = quality
            thumb.url = details['url']
            thumb.width = details.get("width")
            thumb.height = details.get("height")
            thumbnails.append(thumb)
            
        return thumbnails