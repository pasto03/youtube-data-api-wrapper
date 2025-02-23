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
    raw_thumbnails: str = None
    thumbnails: ItemThumbnail = None
    country: Optional[str] = None

@dataclass
class ChannelStatistics:
    hiddenSubscriberCount: bool = None
    viewCount: int = None
    subscriberCount: int = None
    videoCount: int = None

@dataclass
class ChannelItem:
    channelId: str = None
    snippet: ChannelSnippet = None
    statistics: ChannelStatistics = None
    metadata: dict = None


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
            item.metadata = deepcopy(r)
            item.channelId = r['id']
            
            raw_snippet = r.get("snippet")
            if raw_snippet:
                snippet = self._extract_snippet(raw_snippet)
                item.snippet = snippet
            
            raw_statistics = r.get('statistics')
            if raw_statistics:
                statistics = self._extract_statistics(raw_statistics)
                item.statistics = statistics
            
            items.append(item)
        
        return items
    
    def _extract_snippet(self, raw_snippet: dict) -> ChannelSnippet:
        snippet = ChannelSnippet()

        snippet.title = raw_snippet['title']
        snippet.description = raw_snippet['description']
        snippet.customUrl = raw_snippet['customUrl']
        snippet.publishedAt = raw_snippet['publishedAt']
        snippet.raw_thumbnails = raw_snippet['thumbnails']
        snippet.thumbnails = self._extract_thumbnail(raw_snippet['thumbnails'])
        snippet.country = raw_snippet.get('country')

        return snippet
    
    def _extract_statistics(self, raw_statistics: dict) -> ChannelStatistics:
        statistics = ChannelStatistics()

        statistics.hiddenSubscriberCount = raw_statistics.get('hiddenSubscriberCount', -1)
        statistics.viewCount = int(raw_statistics.get('viewCount', -1))
        statistics.subscriberCount = int(raw_statistics.get('subscriberCount', -1))
        statistics.videoCount = int(raw_statistics.get('videoCount', -1))
        
        return statistics