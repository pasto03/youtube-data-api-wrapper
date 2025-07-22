from dataclasses import dataclass
from ..base import BaseContainer


@dataclass
class CaptionSnippet:
    videoId: str = None
    lastUpdated: str = None
    trackKind: str = None
    language: str = None
    name: str = None
    audioTrackType: str = None
    isCC: bool = None
    isLarge: bool = None
    isEasyReader: bool = None
    isDraft: bool = None
    isAutoSynced: bool = None
    status: str = None


@dataclass
class CaptionItem:
    kind: str = "youtube#caption"
    etag: str = None
    id: str = None
    snippet: CaptionSnippet = None


@dataclass
class CaptionsContainer(BaseContainer):
    def __init__(self, raw_items: list[dict]):
        super().__init__(raw_items)
        self.raw_items = raw_items
        self.items: list | list[CaptionItem] = self._extract_item(self.raw_items)

    def _extract_item(self, raw_items: list[dict]) -> list | list[CaptionItem]:
        if len(raw_items) == 0:
            return list()
        
        items = list()
        for r in raw_items:
            item = CaptionItem()
            item.etag = r["etag"]
            item.id = r["id"]
            
            snippet = self._extract_snippet(r["snippet"])

            item.snippet = snippet

            items.append(item)

        return items

    def _extract_snippet(self, raw_snippet) -> CaptionSnippet:
        return CaptionSnippet(**raw_snippet)