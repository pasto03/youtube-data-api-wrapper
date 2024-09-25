from dataclasses import asdict
import os

from youtube_data_api.container.playlist_items.main import PlaylistItemsItem
from youtube_data_api.utils import get_current_time, dict_to_json


class PlaylistItemShipper:
    def __init__(self):
        self.main_records: list[dict] = list()
        self.thumbnails: list[dict] = list()
            
    def invoke(self, items: list[PlaylistItemsItem], output_folder="backup/PlaylistItemShipper", 
               filename=None, backup=True) -> None:
        """
        run the shipper and obtain output
        """
        
        for item in items:
            self.main_records.append(self._extract_details(item))
            self.thumbnails.extend(self._extract_thumbnails(item))
        
        if backup:
            self._handle_backup(self.main_records, suffix=" main records", output_folder=output_folder, 
               filename=filename)
            self._handle_backup(self.thumbnails, suffix=" thumbnails", output_folder=output_folder, 
               filename=filename)
        
#         return self.main_records, self.thumbnails
    
    @staticmethod
    def _handle_backup(records: list[dict], suffix="", output_folder="backup/ChannelShipper", 
               filename=None):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not filename:
            filename = get_current_time() + suffix + ".json"
        records = dict_to_json(records)
        with open(os.path.join(output_folder, filename), "wb") as f:
            f.write(records.encode("utf-8"))
    
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