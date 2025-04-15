from typing import TypeAlias, Literal
from dataclasses import dataclass
from copy import deepcopy

from ..base import ItemThumbnail, BaseContainer

ItemType: TypeAlias = Literal["video", "channel", "playlist"]


# simplify SearchVideoItem to BaseSearchItem
@dataclass
class SearchSnippet:
    """base class for all types of search snippet"""
    publishedAt: str = None
    channelId: str = None
    title: str = None
    description: str = None
    raw_thumbnails: str = None
    thumbnails: ItemThumbnail = None
    channelTitle: str = None

@dataclass
class SearchItem:
    type: ItemType = None
    snippet: SearchSnippet = None
    # must exists
    channelId: str = None
    # either one
    videoId: str = None
    playlistId: str = None
    metadata: dict = None


@dataclass
class SearchContainer(BaseContainer):
    def __init__(self, raw_items: list[dict]):
        super().__init__(raw_items)
        self.raw_items = raw_items
        self.items: list | list[SearchItem] = self._extract_item(self.raw_items)
        
    def _extract_item(self, raw_items) -> list | list[SearchItem]:
        if len(raw_items) == 0:
            return list()
        items = []
        for r in raw_items:
            item = SearchItem()
            item.metadata = deepcopy(r)

            raw_snippet = r.get('snippet')
            if raw_snippet:
                snippet = self._extract_snippet(raw_snippet)
                item.snippet = snippet

                item.channelId = snippet.channelId
                r_id = r['id']
                item.type = r_id['kind'].replace("youtube#", "")
                item.videoId = r_id.get("videoId")
                item.playlistId = r_id.get("playlistId")
            items.append(item)

        return items
    
    def _extract_snippet(self, raw_snippet: dict) -> SearchSnippet:
        snippet = SearchSnippet()
        snippet.title = raw_snippet['title']
        snippet.publishedAt = raw_snippet['publishedAt']
        snippet.channelId = raw_snippet['channelId']
        snippet.description = raw_snippet['description']
        snippet.raw_thumbnails = raw_snippet['thumbnails']
        snippet.thumbnails = self._extract_thumbnail(raw_snippet['thumbnails'])
        snippet.channelTitle = raw_snippet['channelTitle']
        return snippet