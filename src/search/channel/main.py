from dataclasses import dataclass, field
from typing import Type
from ..base import BaseSearchSnippet, BaseSearchItem, BaseSearchResponse


@dataclass
class SearchChannelSnippet(BaseSearchSnippet): ...

@dataclass
class SearchChannelItem:
    snippet: SearchChannelSnippet = None

@dataclass
class SearchChannelResponse(BaseSearchResponse):
    _item_class: Type[SearchChannelItem] = field(init=False)
    _snippet_class: Type[SearchChannelSnippet] = field(init=False)

    def __post_init__(self):
        self._item_class = SearchChannelItem
        self._snippet_class = SearchChannelSnippet
        return super().__post_init__()
    
    def _extract_item(self, raw_items) -> list | list[SearchChannelItem]:
        return super()._extract_item(raw_items)
    
    def _extract_snippet(self, raw_snippet: dict) -> SearchChannelItem:
        return super()._extract_snippet(raw_snippet)