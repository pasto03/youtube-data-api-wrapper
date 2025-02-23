from dataclasses import dataclass, asdict
from typing import Optional
from copy import deepcopy


from ..base import ItemThumbnail, BaseContainer


@dataclass
class VideoItemSnippet:
    publishedAt: str = None
    channelId: str = None
    title: str = None
    description: str = None
    raw_thumbnails: str = None
    thumbnails: ItemThumbnail = None
    channelTitle: str = None
    tags: Optional[list[str]] = None
    categoryId: str = None
    defaultAudioLanguage: Optional[str] = None


@dataclass
class VideoItemDuration:
    h: int = None
    m: int = None
    s: int = None
        
@dataclass
class VideoItemRegionRestriction:
    allowed: Optional[list] = None
    blocked: Optional[list] = None
        
@dataclass
class VideoItemContentDetails:
    duration: VideoItemDuration = None
    dimension: str = None
    definition: str = None
    caption: bool = None
    licensedContent: bool = None
    regionRestriction: VideoItemRegionRestriction = None


@dataclass
class VideoItemStatistics:
    viewCount: int = None
    likeCount: int = None
    favouriteCount: int = None
    commentCount: int = None


@dataclass
class VideoItem:
    videoId: str = None
    snippet: VideoItemSnippet = None
    contentDetails: VideoItemContentDetails = None
    statistics: VideoItemStatistics = None
    metadata: dict = None   # unprocessed data item


class VideosContainer(BaseContainer):
    def __init__(self, raw_items: list[dict]):
        super().__init__(raw_items)
        self.raw_items = raw_items
        self.items: list | list[VideoItem] = self._extract_item(self.raw_items)
            
    def _extract_item(self, raw_items: list[dict]) -> list | list[VideoItem]:
        if len(raw_items) == 0:
            return list()
        items = []
        for r in raw_items:
            item = VideoItem()
            item.metadata = deepcopy(r)
            item.videoId = r['id']
            
            raw_snippet = r.get("snippet")
            if raw_snippet:
                snippet = self._extract_snippet(raw_snippet)
                item.snippet = snippet
            
            raw_contentDetails = r.get('contentDetails')
            if raw_contentDetails:
                contentDetails = self._extract_content_details(raw_contentDetails)
                item.contentDetails = contentDetails
            
            raw_statistics = r.get('statistics')
            if raw_statistics:
                statistics = self._extract_statistics(raw_statistics)
                item.statistics = statistics
            
            items.append(item)
            
        return items
            
    def _extract_snippet(self, raw_snippet: dict) -> VideoItemSnippet:
        snippet = VideoItemSnippet()

        snippet.publishedAt = raw_snippet['publishedAt']
        snippet.channelId = raw_snippet['channelId']
        snippet.title = raw_snippet['title']
        snippet.description = raw_snippet['description']
        snippet.raw_thumbnails = raw_snippet['thumbnails']
        snippet.thumbnails = self._extract_thumbnail(raw_snippet['thumbnails'])
        snippet.channelTitle = raw_snippet['channelTitle']
        snippet.tags = raw_snippet.get("tags")
        categoryId = raw_snippet.get('categoryId')
        snippet.categoryId = None if not categoryId else int(categoryId)
        snippet.defaultAudioLanguage = raw_snippet.get('defaultAudioLanguage')
        
        return snippet
    
    def _extract_content_details(self, raw_contentDetails) -> VideoItemContentDetails:
        contentDetails = VideoItemContentDetails()

        contentDetails.duration = raw_contentDetails['duration']
        contentDetails.dimension = raw_contentDetails['dimension']
        contentDetails.definition = raw_contentDetails['definition']
        contentDetails.caption = True if raw_contentDetails['caption'] == "true" else False
        contentDetails.licensedContent = raw_contentDetails['licensedContent']

        regionRestriction = VideoItemRegionRestriction()
        raw_regionRestriction = raw_contentDetails.get('regionRestriction')
        if raw_regionRestriction:
            regionRestriction.allowed = raw_regionRestriction.get("allowed")
            regionRestriction.blocked = raw_regionRestriction.get("blocked")
        contentDetails.regionRestriction = regionRestriction
        
        return contentDetails
    
    def _extract_statistics(self, raw_statistics) -> VideoItemStatistics:
        statistics = VideoItemStatistics()

        statistics.viewCount = int(raw_statistics.get('viewCount', -1))
        statistics.likeCount = int(raw_statistics.get('likeCount', -1))
        statistics.favouriteCount = int(raw_statistics.get('favoriteCount', -1))
        statistics.commentCount = int(raw_statistics.get('commentCount', -1))
        
        return statistics