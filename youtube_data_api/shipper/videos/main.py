from dataclasses import asdict

from youtube_data_api.container.videos.main import VideoItem
from youtube_data_api.shipper.base import BaseShipper


class VideoShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.output_folder = "backup/VideoShipper"
    
    def invoke(self, items: list[VideoItem], output_folder=None, backup=True) -> None:
        """
        run the shipper and obtain output
        """
        return super().invoke(items=items, output_folder=output_folder, backup=backup)

    @staticmethod
    def _extract_details(item: VideoItem):
        record = dict()

        # 1. videoId(primary key)
        record['videoId'] = item.videoId

        # 2. snippets
        snippet = item.snippet
        record['title'] = snippet.title
        record['description'] = snippet.description
        record['publishedAt'] = snippet.publishedAt
        record['channelId'] = snippet.channelId
        record['channelTitle'] = snippet.channelTitle

        tags = snippet.tags
        tags = "" if not tags else "#" + " #".join(tags)
        record['tags'] = tags
        record['categoryId'] = snippet.categoryId
        record['defaultAudioLanguage'] = snippet.defaultAudioLanguage

        # 3. contentDetails
        details = item.contentDetails
        record['duration'] = details.duration
        record['caption'] = details.caption
        record['licensedContent'] = details.licensedContent

        # 4. statistics
        stats = item.statistics
        record['favouriteCount'] = stats.favouriteCount
        record['commentCount'] = stats.commentCount
        record["viewCount"] = stats.viewCount
        record["likeCount"] = stats.likeCount

        return record
    
    @staticmethod
    def _extract_thumbnails(item: VideoItem) -> list[dict]:
        """
        return a list of dict of thumbnails
        """
        records = list()

        thumbnails = item.snippet.thumbnails
        for tn in thumbnails:
            record = dict()

            # 1. videoId(foreign primary key)
            record['videoId'] = item.videoId

            # 2. thumbnail
            record.update(asdict(tn))
            records.append(record)

        return records