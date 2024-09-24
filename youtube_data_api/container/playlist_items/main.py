from dataclasses import dataclass, asdict
from copy import deepcopy

from ..base import ItemThumbnail, BaseContainer


@dataclass
class PlaylistItemsSnippet:
    publishedAt: str = None
    channelId: str = None
    title: str = None
    description: str = None
    raw_thumbnails: str = None
    thumbnails: ItemThumbnail = None
    channelTitle: str = None
    playlistId: str = None
    position: int = None
    videoId: str = None


@dataclass
class PlaylistItemsContentDetails:
    videoId: str = None
    videoPublishedAt: str = None


@dataclass
class PlaylistItemsItem:
    videoId: str = None
    playlistId: str = None
    snippet: PlaylistItemsSnippet = None
    contentDetails: PlaylistItemsContentDetails = None
    metadata: dict = None


@dataclass
class PlaylistItemsContainer(BaseContainer):
    def __init__(self, raw_items: list[dict]):
        super().__init__(raw_items)
        self.raw_items = raw_items
        self.items: list | list[PlaylistItemsItem] = self._extract_item(self.raw_items)
            
    def _extract_item(self, raw_items) -> list | list[PlaylistItemsItem]:
        if len(raw_items) == 0:
            return list()
        items = []
        for r in raw_items:
            item = PlaylistItemsItem()
            item.metadata = deepcopy(r)

            videoId = r['snippet']['resourceId']['videoId']
            
            item.videoId = videoId
            item.playlistId = r['snippet']['playlistId']

            # 1. snippet
            raw_snippet = r['snippet'] 
            snippet = self._extract_snippet(raw_snippet)

            item.snippet = snippet

            # 2. contentDetails
            raw_contentDetails = r['contentDetails']
            contentDetails = self._extract_content_details(raw_contentDetails)

            item.contentDetails = contentDetails
            
            items.append(item)
        
        return items
    
    def _extract_snippet(self, raw_snippet: dict) -> PlaylistItemsSnippet:
        """extract snippet part from response"""
        snippet = PlaylistItemsSnippet()

        snippet.publishedAt = raw_snippet['publishedAt']
        snippet.channelId = raw_snippet['channelId']
        snippet.title = raw_snippet['title']
        snippet.description = raw_snippet['description']
        snippet.raw_thumbnails = raw_snippet['thumbnails']
        snippet.thumbnails = self._extract_thumbnail(raw_snippet['thumbnails'])
        snippet.channelTitle = raw_snippet['channelTitle']
        snippet.playlistId = raw_snippet['playlistId']
        snippet.position = raw_snippet['position']
        snippet.videoId = raw_snippet['resourceId']['videoId']
        
        return snippet
    
    def _extract_content_details(self, raw_contentDetails: dict) -> PlaylistItemsContentDetails:
        """extract contentDetails part from response"""
        contentDetails = PlaylistItemsContentDetails()
        contentDetails.videoId = raw_contentDetails['videoId']
        contentDetails.videoPublishedAt = raw_contentDetails.get('videoPublishedAt')
        return contentDetails