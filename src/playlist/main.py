from dataclasses import dataclass, asdict
from typing import Optional

from src.common.thumbnail import ItemThumbnail
from src.base.parser import BaseResponse


@dataclass
class PlaylistSnippet:
    publishedAt: str = None
    channelId: str = None
    title: str = None
    description: str = None
    raw_thumbnails: str = None
    thumbnails: ItemThumbnail = None
    channelTitle: str = None
        
@dataclass
class PlaylistContentDetails:
    itemCount: int = None


@dataclass
class PlaylistsItem:
    playlistId: str = None
    snippet: PlaylistSnippet = None
    contentDetails: PlaylistContentDetails = None

@dataclass
class PlaylistsResponse(BaseResponse):
    def __init__(self, response: dict):
        super().__init__(response)
        self.playlistId: str = None
        self.nextPageToken: Optional[str] = response.get("nextPageToken")
        self.prevPageToken: Optional[str] = response.get("prevPageToken")
        self.items: list | list[PlaylistsItem] = self._extract_item(self.raw_items)
        self.pageInfo: dict = response['pageInfo']
            
    def _extract_item(self, raw_items) -> list | list[PlaylistsItem]:
        if len(raw_items) == 0:
            return list()
        items = []
        for r in raw_items:
            playlists_item = PlaylistsItem()

            playlists_item.playlistId = r['id']
            self.playlistId = r['id']

            # 1. snippet
            raw_snippet = r['snippet'] 
            snippet = self._extract_snippet(raw_snippet)

            playlists_item.snippet = snippet

            # 2. contentDetails
            raw_contentDetails = r['contentDetails']
            contentDetails = self._extract_content_details(raw_contentDetails)

            playlists_item.contentDetails = contentDetails
            
            items.append(playlists_item)
        
        return items
    
    def _extract_snippet(self, raw_snippet: dict) -> PlaylistSnippet:
        """extract snippet part from response"""
        snippet = PlaylistSnippet()

        snippet.publishedAt = raw_snippet['publishedAt']
        snippet.channelId = raw_snippet['channelId']
        snippet.title = raw_snippet['title']
        snippet.description = raw_snippet['description']
        snippet.raw_thumbnails = raw_snippet['thumbnails']
        snippet.thumbnails = self._extract_thumbnail(raw_snippet['thumbnails'])
        snippet.channelTitle = raw_snippet['channelTitle']
        
        return snippet
    
    def _extract_content_details(self, raw_contentDetails: dict) -> PlaylistContentDetails:
        """extract contentDetails part from response"""
        contentDetails = PlaylistContentDetails()
        contentDetails.itemCount = raw_contentDetails['itemCount']
        return contentDetails