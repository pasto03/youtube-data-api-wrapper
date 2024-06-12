from dataclasses import dataclass
from ...common.thumbnail import ItemThumbnail


@dataclass
class BaseItems: ...


@dataclass
class BaseResponse:
    """
    base response parser class
    
    set self.items = self._extract_item(self.raw_items) when inherited
    """
    response: dict
    raw_items: list | None = None
    
    def __init__(self, response: dict):
        self.response = response
        self.raw_items = response.get("items")
        
    def _extract_item(self, raw_items):
        raise NotImplementedError
    
    # we assue this function is universal across APIs
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