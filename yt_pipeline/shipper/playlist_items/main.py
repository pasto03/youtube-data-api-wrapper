from dataclasses import asdict

from yt_pipeline.container.playlist_items.main import PlaylistItemsItem
from ..base import BaseShipper


class PlaylistItemShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.output_folder = "backup/PlaylistItemShipper"
    
    def invoke(self, items: list[PlaylistItemsItem], output_folder=None, backup=True) -> None:
        return super().invoke(items=items, output_folder=output_folder, backup=backup)
    
    def _extract_details(self, item: PlaylistItemsItem) -> None:
        record = dict()

        record['kind'] = item.kind
        record['etag'] = item.etag
        record['id'] = item.id

        snippet_item = asdict(item.snippet)
        thumbnails_item = snippet_item.pop("thumbnails")

        self.thumbnails[item.id] = thumbnails_item

        record.update(snippet_item)

        record.update(asdict(item.contentDetails))

        self.main_records.append(record)