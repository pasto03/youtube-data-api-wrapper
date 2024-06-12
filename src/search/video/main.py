from dataclasses import dataclass, field
from typing import Type

from ..base import BaseSearchSnippet, BaseSearchItem, BaseSearchResponse


@dataclass
class SearchVideoSnippet(BaseSearchSnippet):
    videoId: str = None

@dataclass
class SearchVideoItem(BaseSearchItem):
    snippet: SearchVideoSnippet = None

@dataclass
class SearchVideoResponse(BaseSearchResponse):
    _item_class: Type[SearchVideoItem] = field(init=False)
    _snippet_class: Type[SearchVideoSnippet] = field(init=False)

    def __post_init__(self):
        self._item_class = SearchVideoItem
        self._snippet_class = SearchVideoSnippet
        return super().__post_init__()
    
    def _extract_item(self, raw_items) -> list | list[SearchVideoItem]:
        if len(raw_items) == 0:
            return list()
        items = []
        for r in raw_items:
            id = r['id']
            item = SearchVideoItem()
            raw_snippet = r['snippet']
            if raw_snippet:
                snippet = self._extract_snippet(raw_snippet)
                snippet.videoId = id['videoId']
                item.snippet = snippet  
            items.append(item)

        return items
    
    def _extract_snippet(self, raw_snippet: dict) -> SearchVideoSnippet:
        return super()._extract_snippet(raw_snippet)