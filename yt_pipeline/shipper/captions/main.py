from dataclasses import asdict

from yt_pipeline.container.captions.main import CaptionItem
from yt_pipeline.shipper.base import BaseShipper


class CaptionsShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.thumbnails = None
        self.output_folder = "backup/CaptionsShipper"

    def invoke(self, items: list[CaptionItem], output_folder=None, backup=True):
        for item in items:
            self.main_records.append(self._extract_details(item))

        if backup:
            self._handle_backup(self.main_records, suffix=" main records", output_folder=output_folder)

    @staticmethod
    def _extract_details(item: CaptionItem) -> dict:
        record = dict()
        record["kind"] = item.kind
        record["etag"] = item.etag
        record["id"] = item.id

        snippet = item.snippet
        record.update(asdict(snippet))

        return record