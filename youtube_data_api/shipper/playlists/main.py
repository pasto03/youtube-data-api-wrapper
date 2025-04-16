from dataclasses import asdict

from youtube_data_api.container.playlists.main import PlaylistsItem
from ..base import BaseShipper


class PlaylistShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.output_folder = "backup/PlaylistShipper"
    
    def invoke(self, items: list[PlaylistsItem], output_folder=None, backup=True) -> None:
        return super().invoke(items=items, output_folder=output_folder, backup=backup)
    
    def _extract_details(self, item: PlaylistsItem) -> None:
        record = dict()

        record['kind'] = item.kind
        record['etag'] = item.etag
        record['id'] = item.id

        snippet_item = asdict(item.snippet)
        thumbnails_item = snippet_item.pop("thumbnails")

        self.thumbnails[item.id] = thumbnails_item

        record.update(snippet_item)

        record['itemCount'] = item.contentDetails.itemCount

        self.main_records.append(record)