from dataclasses import dataclass, field
from typing import Type
from ..base import BaseSearchSnippet, BaseSearchItem, BaseSearchResponse


@dataclass
class SearchPlaylistSnippet(BaseSearchSnippet):
    playlistId: str = None

@dataclass
class SearchPlaylistItem(BaseSearchItem):
    snippet: SearchPlaylistSnippet = None
        
@dataclass
class SearchPlaylistResponse(BaseSearchResponse):
    _item_class: Type[SearchPlaylistItem] = field(init=False)
    _snippet_class: Type[SearchPlaylistSnippet] = field(init=False)

    def __post_init__(self):
        self._item_class = SearchPlaylistItem
        self._snippet_class = SearchPlaylistSnippet
        return super().__post_init__()
    
    def _extract_item(self, raw_items) -> list | list[SearchPlaylistItem]:
        if len(raw_items) == 0:
            return list()
        items = []
        for r in raw_items:
            id = r['id']
            item = SearchPlaylistItem()
            raw_snippet = r['snippet']
            if raw_snippet:
                snippet = self._extract_snippet(raw_snippet)
                snippet.playlistId = id['playlistId']
                item.snippet = snippet
            items.append(item)

        return items
    
    def _extract_snippet(self, raw_snippet: dict) -> SearchPlaylistSnippet:
        return super()._extract_snippet(raw_snippet)