from dataclasses import asdict

from yt_pipeline.container.videos.main import VideoItem
from yt_pipeline.shipper.base import BaseShipper


class VideoShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.output_folder = "backup/VideoShipper"
    
    def invoke(self, items: list[VideoItem], output_folder=None, backup=True):
        return super().invoke(items, output_folder, backup)

    def _extract_details(self, item: VideoItem) -> None:
        record = dict()

        record['kind'] = item.kind
        record['etag'] = item.etag
        record['id'] = item.id

        # 1. snippets
        snippet_item = asdict(item.snippet)
        thumbnails_item: list[dict] = snippet_item.pop("thumbnails")

        # thumbnails for corresponding videoId
        self.thumbnails[item.id] = thumbnails_item

        record.update(snippet_item)

        tags = record.get("tags")
        if tags:
            record['tags'] = "#" + " #".join(tags)

        # 2. contentDetails
        content_details_item = asdict(item.contentDetails)
        region_restriction_item = content_details_item.get("regionRestriction")

        # this attribute will be removed for ease of flattening (losing details)
        if region_restriction_item:
            content_details_item.pop("regionRestriction")

        record.update(content_details_item)

        # 3. statistics
        record.update(asdict(item.statistics))

        self.main_records.append(record)