from ...base.parser import BaseResponse
from typing import Type, Optional
from dataclasses import field, dataclass

from ...common.thumbnail import ItemThumbnail

# simplify SearchVideoItem to BaseSearchItem
@dataclass
class BaseSearchSnippet:
    """base class for all types of search snippet"""
    publishedAt: str = None
    channelId: str = None
    title: str = None
    description: str = None
    raw_thumbnails: str = None
    thumbnails: ItemThumbnail = None
    channelTitle: str = None

@dataclass
class BaseSearchItem:
    snippet: BaseSearchSnippet = None

@dataclass
class BaseSearchResponse(BaseResponse):
    """base class for all types of search response"""
    response: dict
    nextPageToken: Optional[str] = field(init=False)
    prevPageToken: Optional[str] = field(init=False)
    pageInfo: dict = field(init=False)
    items: list | list[BaseSearchItem] = field(init=False)
    _item_class: Type[BaseSearchItem] = field(init=False)
    _snippet_class: Type[BaseSearchSnippet] = field(init=False)
        
    def __post_init__(self):
        super().__init__(self.response)
        self.nextPageToken = self.response.get("nextPageToken")
        self.prevPageToken = self.response.get("prevPageToken")
        self.pageInfo = self.response['pageInfo']
        self.items = self._extract_item(self.response.get('items', []))
        self._item_class = BaseSearchItem
        self._snippet_class = BaseSearchSnippet
        
    def _extract_item(self, raw_items) -> list | list[BaseSearchItem]:
        if len(raw_items) == 0:
            return list()
        items = []
        for r in raw_items:
            item = self._item_class()

            raw_snippet = r.get('snippet')
            if raw_snippet:
                snippet = self._extract_snippet(raw_snippet)
                item.snippet = snippet
            items.append(item)

        return items
    
    def _extract_snippet(self, raw_snippet: dict) -> BaseSearchSnippet:
        snippet = self._snippet_class()
        snippet.title = raw_snippet['title']
        snippet.publishedAt = raw_snippet['publishedAt']
        snippet.channelId = raw_snippet['channelId']
        snippet.description = raw_snippet['description']
        snippet.raw_thumbnails = raw_snippet['thumbnails']
        snippet.thumbnails = self._extract_thumbnail(raw_snippet['thumbnails'])
        snippet.channelTitle = raw_snippet['channelTitle']
        return snippet