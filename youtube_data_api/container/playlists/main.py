from dataclasses import dataclass
from copy import deepcopy

from ..base import ItemThumbnail, BaseContainer


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
    metadata: dict = None

@dataclass
class PlaylistsContainer(BaseContainer):
    def __init__(self, raw_items: list[dict]):
        super().__init__(raw_items)
        self.raw_items = raw_items
        self.items: list | list[PlaylistsItem] = self._extract_item(self.raw_items)
            
    def _extract_item(self, raw_items: list[dict]) -> list | list[PlaylistsItem]:
        if len(raw_items) == 0:
            return list()
        items = []
        count = 0
        for r in raw_items:
            item = PlaylistsItem()
            item.metadata = deepcopy(r)

            id = r.get("id")
            if not id:
                print(r)
            item.playlistId = r['id']

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