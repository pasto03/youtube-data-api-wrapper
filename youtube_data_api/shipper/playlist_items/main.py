from dataclasses import asdict

from youtube_data_api.container.playlist_items.main import PlaylistItemsItem
from ..base import BaseShipper


class PlaylistItemShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.output_folder = "backup/PlaylistItemShipper"
    
    def invoke(self, items: list[PlaylistItemsItem], output_folder=None, backup=True) -> None:
        """
        run the shipper and obtain output
        """
        return super().invoke(items=items, output_folder=output_folder, backup=backup)
    
    @staticmethod
    def _extract_details(item: PlaylistItemsItem) -> dict:
        record = dict()

        # 1. videoId(primary key) + playlistId
        record['videoId'] = item.videoId
        record['playlistId'] = item.playlistId

        # 2. snippets
        snippet = item.snippet
        record['title'] = snippet.title
        record['description'] = snippet.description
        record['publishedAt'] = snippet.publishedAt
        record['channelId'] = snippet.channelId
        record['channelTitle'] = snippet.channelTitle
        record['position'] = snippet.position

        return record
    
    @staticmethod
    def _extract_thumbnails(item: PlaylistItemsItem) -> list[dict]:
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