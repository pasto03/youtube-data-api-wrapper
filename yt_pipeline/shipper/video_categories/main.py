from yt_pipeline.container.video_categories.main import VideoCategoryItem
from yt_pipeline.shipper.base import BaseShipper


class VideoCategoriesShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.thumbnails = None
        self.output_folder = "backup/VideoCategoriesShipper"

    def invoke(self, items: list[VideoCategoryItem], output_folder=None, backup=True):
        for item in items:
            self.main_records.append(self._extract_details(item))

        if backup:
            self._handle_backup(self.main_records, suffix=" main records", output_folder=output_folder)

    @staticmethod
    def _extract_details(item: VideoCategoryItem) -> dict:
        record = dict()
        record["kind"] = item.kind
        record["etag"] = item.etag
        record["id"] = item.id

        snippet = item.snippet
        record["title"] = snippet.title
        record["assignable"] = snippet.assignable
        record["channelId"] = snippet.channelId

        return record