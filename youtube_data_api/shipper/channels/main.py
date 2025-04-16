from dataclasses import asdict

from youtube_data_api.container.channels.main import ChannelItem
from ..base import BaseShipper


class ChannelShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.output_folder = "backup/ChannelShipper"
    
    def invoke(self, items: list[ChannelItem], output_folder=None, backup=True):
        return super().invoke(items, output_folder, backup)
    
    def _extract_details(self, item: ChannelItem) -> None:
        record = dict()

        record['kind'] = item.kind
        record['etag'] = item.etag
        record['id'] = item.id

        snippet_item = asdict(item.snippet)
        thumbnails_item: list[dict] = snippet_item.pop("thumbnails")

        self.thumbnails[item.id] = thumbnails_item

        record.update(snippet_item)

        record.update(asdict(item.statistics))

        self.main_records.append(record)