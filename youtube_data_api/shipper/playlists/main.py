from dataclasses import asdict

from youtube_data_api.container.playlists.main import PlaylistsItem
from ..base import BaseShipper


class PlaylistShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.output_folder = "backup/PlaylistShipper"
    
    def invoke(self, items: list[PlaylistsItem], output_folder=None, backup=True) -> None:
        """
        run the shipper and obtain output
        """
        return super().invoke(items=items, output_folder=output_folder, backup=backup)
    
    @staticmethod
    def _extract_details(item: PlaylistsItem) -> dict:
        record = dict()

        # 1. playlistId(primary key)
        record['playlistId'] = item.playlistId

        # 2. snippets
        snippet = item.snippet
        record['title'] = snippet.title
        record['description'] = snippet.description
        record['publishedAt'] = snippet.publishedAt
        record['channelId'] = snippet.channelId
        record['channelTitle'] = snippet.channelTitle

        # 3. contentDetails
        record['itemCount'] = item.contentDetails.itemCount

        return record
    
    @staticmethod
    def _extract_thumbnails(item: PlaylistsItem) -> list[dict]:
        """
        return a list of dict of thumbnails
        """
        records = list()

        thumbnails = item.snippet.thumbnails
        for tn in thumbnails:
            record = dict()

            # 1. playlistId(foreign primary key)
            record['playlistId'] = item.playlistId

            # 2. thumbnail
            record.update(asdict(tn))
            records.append(record)

        return records