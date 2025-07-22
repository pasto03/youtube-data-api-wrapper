from typing import TypeAlias, Literal
from dataclasses import dataclass
from copy import deepcopy

from ..base import ItemThumbnail, BaseContainer


@dataclass
class SearchSnippet:
    """base class for all types of search snippet"""
    publishedAt: str = None
    channelId: str = None
    title: str = None
    description: str = None
    thumbnails: list[ItemThumbnail] = None
    channelTitle: str = None
    liveBroadcastContent: str = None


@dataclass
class SearchId:
    kind: str = None
    videoId: str = None
    channelId: str = None
    playlistId: str = None


@dataclass
class SearchItem:
    kind: str = "youtube#searchResult"
    etag: str = None
    id: SearchId = None
    snippet: SearchSnippet = None


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

            item.etag = r["etag"]

            item.id = SearchId(**r["id"])

            item.snippet = self._extract_snippet(deepcopy(r["snippet"]))

            items.append(item)

        return items
    
    def _extract_snippet(self, raw_snippet: dict) -> SearchSnippet:
        thumbnails_item = raw_snippet.pop("thumbnails")

        # remove redundants
        raw_snippet.pop("publishTime")

        snippet = SearchSnippet(**raw_snippet)
        snippet.thumbnails = self._extract_thumbnail(thumbnails_item)

        return snippet