from dataclasses import asdict

from youtube_data_api.container.search.main import SearchItem
from youtube_data_api.shipper.base import BaseShipper


class SearchShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.output_folder = "backup/SearchShipper"
    
    def invoke(self, items: list[SearchItem], output_folder=None, backup=True) -> None:
        """
        run the shipper and obtain output
        """
        return super().invoke(items=items, output_folder=output_folder, backup=backup)
    
    @staticmethod
    def _extract_details(item: SearchItem):
        record = dict()

        # 1. type
        record['type'] = item.type

        # 2. snippets
        snippet = item.snippet
        record['title'] = snippet.title
        record['description'] = snippet.description
        record['publishedAt'] = snippet.publishedAt
        record['channelId'] = snippet.channelId
        record['channelTitle'] = snippet.channelTitle

        # 3. contentDetails
        record['videoId'] = item.videoId
        record['playlistId'] = item.playlistId

        return record
    
    @staticmethod
    def _extract_thumbnails(item: SearchItem) -> list[dict]:
        """
        return a list of dict of thumbnails
        """
        records = list()

        thumbnails = item.snippet.thumbnails
        for tn in thumbnails:
            record = dict()
            # 1. type
            record['type'] = item.type

            # 1. id
            record['playlistId'] = item.playlistId
            record['videoId'] = item.videoId
            record['channelId'] = item.channelId

            # 2. thumbnail
            record.update(asdict(tn))
            records.append(record)

        return records