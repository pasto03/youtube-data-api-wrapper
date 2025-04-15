from dataclasses import dataclass

from ..base import BaseContainer

@dataclass
class VideoCategorySnippet:
    channelId: str = "UCBR8-60-B28hp2BmDPdntcQ"
    title: str = None
    assignable: bool = None

@dataclass
class VideoCategoryItem:
    kind: str = "youtube#videoCategory"
    etag: str = None
    id: str = None
    snippet: VideoCategorySnippet = None


@dataclass
class VideoCategoriesContainer(BaseContainer):
    def __init__(self, raw_items: list[dict]):
        super().__init__(raw_items)
        self.raw_items = raw_items
        self.items: list | list[VideoCategoryItem] = self._extract_item(self.raw_items)

    def _extract_item(self, raw_items: list[dict]) -> list | list[VideoCategoryItem]:
        if len(raw_items) == 0:
            return list()
        
        items = list()
        for r in raw_items:
            item = VideoCategoryItem()
            item.etag = r["etag"]
            item.id = r["id"]
            
            snippet = self._extract_snippet(r["snippet"])

            item.snippet = snippet

            items.append(item)

        return items

    def _extract_snippet(self, raw_snippet) -> VideoCategorySnippet:
        snippet = VideoCategorySnippet()
        snippet.title = raw_snippet["title"]
        snippet.assignable = raw_snippet["assignable"]

        return snippet