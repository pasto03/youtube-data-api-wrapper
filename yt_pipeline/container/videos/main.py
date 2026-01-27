from dataclasses import dataclass, asdict
from typing import Optional
from copy import deepcopy

import warnings


from ..base import ItemThumbnail, BaseContainer


@dataclass
class VideoItemSnippet:
    publishedAt: str = None
    channelId: str = None
    title: str = None
    description: str = None
    thumbnails: list[ItemThumbnail] = None
    channelTitle: str = None
    tags: Optional[list[str]] = None
    categoryId: str = None
    defaultLanguage: Optional[str] = None
    defaultAudioLanguage: Optional[str] = None


@dataclass
class VideoItemDuration:
    warnings.warn(
        "VideoItemDuration() is deprecated and will be removed in a future version.",
        DeprecationWarning,
        stacklevel=2
    )
    h: int = None
    m: int = None
    s: int = None
        

@dataclass
class VideoItemRegionRestriction:
    allowed: Optional[list] = None
    blocked: Optional[list] = None
        

@dataclass
class VideoItemContentDetails:
    duration: str = None
    dimension: str = None
    definition: str = None
    caption: str = None
    licensedContent: bool = None
    regionRestriction: VideoItemRegionRestriction = None


@dataclass
class VideoItemStatistics:
    viewCount: int = None
    likeCount: int = None
    favoriteCount: int = None
    commentCount: int = None


@dataclass
class VideoItem:
    kind: str = "youtube#video"
    etag: str = None
    id: str = None
    snippet: VideoItemSnippet = None
    contentDetails: VideoItemContentDetails = None
    statistics: VideoItemStatistics = None


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

            item.etag = r["etag"]
            item.id = r["id"]
            
            snippet_item = r["snippet"]
            item.snippet = self._extract_snippet(deepcopy(snippet_item))
            
            content_details_item = r['contentDetails']
            item.contentDetails = self._extract_content_details(deepcopy(content_details_item))
            
            statistics_item = r['statistics']
            item.statistics = self._extract_statistics(deepcopy(statistics_item))
            
            items.append(item)
            
        return items
            
    def _extract_snippet(self, raw_snippet: dict) -> VideoItemSnippet:
        thumbnails_item = raw_snippet.pop("thumbnails")

        # remove redundant
        raw_snippet.pop("liveBroadcastContent")
        raw_snippet.pop("localized")

        snippet = VideoItemSnippet(**raw_snippet)
        snippet.thumbnails = self._extract_thumbnail(thumbnails_item)

        return snippet
    
    def _extract_content_details(self, content_details_item: dict) -> VideoItemContentDetails:

        region_restriction_item = content_details_item.get("regionRestriction")
        region_restriction = None

        if region_restriction_item:
            region_restriction = VideoItemRegionRestriction(**region_restriction_item)
            content_details_item.pop('regionRestriction')

        # remove redundant
        content_details_item.pop("contentRating")
        content_details_item.pop("projection")

        contentDetails = VideoItemContentDetails(**content_details_item)
        contentDetails.regionRestriction = region_restriction
        
        return contentDetails

    def _extract_statistics(self, statistics_item: dict) -> VideoItemStatistics:
        """
        extract statistics from the raw item and convert to int if possible
        """
        statistics = VideoItemStatistics()
        statistics.viewCount = int(statistics_item.get("viewCount", 0))
        statistics.likeCount = int(statistics_item.get("likeCount", 0))
        statistics.favoriteCount = int(statistics_item.get("favoriteCount", 0))
        statistics.commentCount = int(statistics_item.get("commentCount", 0))
        return statistics