from dataclasses import dataclass, asdict
from typing import Optional
from copy import deepcopy

from ..base import ItemThumbnail, BaseContainer
    
@dataclass
class ChannelSnippet:
    title: str = None
    description: str = None
    customUrl: str = None
    publishedAt: str = None
    thumbnails: list[ItemThumbnail] = None
    defaultLanguage: str = None
    country: Optional[str] = None

@dataclass
class ChannelStatistics:
    viewCount: str = None
    subscriberCount: str = None
    hiddenSubscriberCount: bool = None
    videoCount: str = None

@dataclass
class ChannelItem:
    kind: str = "youtube#channel"
    etag: str = None
    id: str = None
    snippet: ChannelSnippet = None
    statistics: ChannelStatistics = None


class ChannelsContainer(BaseContainer):
    def __init__(self, raw_items: list[dict]):
        super().__init__(raw_items)
        self.raw_items = raw_items
        self.items: list | list[ChannelItem] = self._extract_item(self.raw_items)
 
    def _extract_item(self, raw_items: list[dict]) -> list | list[ChannelItem]:
        if len(raw_items) == 0:
            return list()
        
        items = []
        for r in raw_items:
            item = ChannelItem()

            item.kind = r['kind']
            item.etag = r['etag']
            item.id = r['id']

            item.snippet = self._extract_snippet(deepcopy(r['snippet']))

            item.statistics = ChannelStatistics(**r['statistics'])

            items.append(item)
        
        return items
    
    def _extract_snippet(self, raw_snippet: dict) -> ChannelSnippet:
        thumbnails_item = raw_snippet.pop("thumbnails")

        # remove redundant
        raw_snippet.pop("localized")

        snippet = ChannelSnippet(**raw_snippet)
        snippet.thumbnails = self._extract_thumbnail(thumbnails_item)

        return snippet