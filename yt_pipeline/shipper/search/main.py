from dataclasses import asdict

from yt_pipeline.container.search.main import SearchItem
from yt_pipeline.shipper.base import BaseShipper


class SearchShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.output_folder = "backup/SearchShipper"
    
    def invoke(self, items: list[SearchItem], output_folder=None, backup=True):
        return super().invoke(items, output_folder, backup)
    
    def _extract_details(self, item: SearchItem) -> None:
        record = dict()

        record['kind'] = item.kind
        record['etag'] = item.etag

        id_item = asdict(item.id)
        record.update(id_item)

        snippet_item = asdict(item.snippet)
        thumbnails_item = snippet_item.pop("thumbnails")

        dominant_id = item.id.channelId or item.id.playlistId or item.id.videoId
        self.thumbnails[dominant_id] = thumbnails_item

        record.update(snippet_item)

        self.main_records.append(record)