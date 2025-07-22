from dataclasses import dataclass
from copy import deepcopy
from typing import Optional

from ..base import ItemThumbnail, BaseContainer


@dataclass
class PlaylistSnippet:
    publishedAt: str = None
    channelId: str = None
    title: str = None
    description: str = None
    thumbnails: list[ItemThumbnail] = None
    channelTitle: str = None
    defaultLanguage: str = None
        
@dataclass
class PlaylistContentDetails:
    itemCount: int = None


@dataclass
class PlaylistsItem:
    kind: str = "youtube#playlist"
    etag: str = None
    id: str = None
    snippet: PlaylistSnippet = None
    contentDetails: PlaylistContentDetails = None


@dataclass
class PlaylistsContainer(BaseContainer):
    def __init__(self, raw_items: list[dict]):
        super().__init__(raw_items)
        self.raw_items = raw_items
        self.items: list | list[PlaylistsItem] = self._extract_item(self.raw_items)
            
    def _extract_item(self, raw_items: list[dict]) -> list | list[PlaylistsItem]:
        if len(raw_items) == 0:
            return list()
        
        items = []
        for r in raw_items:
            item = PlaylistsItem()

            item.etag = r["etag"]
            item.id = r["id"]

            snippet_item = r["snippet"]
            item.snippet = self._extract_snippet(deepcopy(snippet_item))

            item.contentDetails = PlaylistContentDetails(itemCount=r["contentDetails"]["itemCount"])

            items.append(item)
        
        return items
    
    def _extract_snippet(self, raw_snippet: dict) -> PlaylistSnippet:
        thumbnails_item = raw_snippet.pop("thumbnails")

        # remove redundant
        if raw_snippet.get("localized"):
            raw_snippet.pop("localized")

        snippet = PlaylistSnippet(**raw_snippet)
        snippet.thumbnails = self._extract_thumbnail(thumbnails_item)

        return snippet