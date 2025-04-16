from dataclasses import dataclass, asdict
from copy import deepcopy

from ..base import ItemThumbnail, BaseContainer


@dataclass
class PlaylistItemsSnippet:
    publishedAt: str = None
    channelId: str = None
    title: str = None
    description: str = None
    thumbnails: list[ItemThumbnail] = None
    channelTitle: str = None
    playlistId: str = None
    position: int = None


@dataclass
class PlaylistItemsContentDetails:
    videoId: str = None
    videoPublishedAt: str = None


@dataclass
class PlaylistItemsItem:
    kind: str = "youtube#playlistItem"
    etag: str = None
    id: str = None
    snippet: PlaylistItemsSnippet = None
    contentDetails: PlaylistItemsContentDetails = None


@dataclass
class PlaylistItemsContainer(BaseContainer):
    def __init__(self, raw_items: list[dict]):
        super().__init__(raw_items)
        self.raw_items = raw_items
        self.items: list | list[PlaylistItemsItem] = self._extract_item(self.raw_items)
            
    def _extract_item(self, raw_items) -> list | list[PlaylistItemsItem]:
        if len(raw_items) == 0:
            return list()
        
        items = []
        for r in raw_items:
            item = PlaylistItemsItem()

            item.etag = r["etag"]
            item.id = r["id"]

            snippet_item = r["snippet"]
            item.snippet = self._extract_snippet(deepcopy(snippet_item))

            item.contentDetails = PlaylistItemsContentDetails(**r["contentDetails"])
            
            items.append(item)
        
        return items
    
    def _extract_snippet(self, raw_snippet: dict) -> PlaylistItemsSnippet:
        thumbnails_item = raw_snippet.pop("thumbnails")

        # remove redundant
        raw_snippet.pop("resourceId")
        raw_snippet.pop("videoOwnerChannelTitle")
        raw_snippet.pop("videoOwnerChannelId")

        snippet = PlaylistItemsSnippet(**raw_snippet)
        snippet.thumbnails = self._extract_thumbnail(thumbnails_item)

        return snippet