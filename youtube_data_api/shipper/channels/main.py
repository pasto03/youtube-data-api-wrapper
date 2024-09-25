import os
from dataclasses import asdict

from youtube_data_api.container.channels.main import ChannelItem
from youtube_data_api.utils import get_current_time, dict_to_json


class ChannelShipper:
    def __init__(self):
        self.main_records: list[dict] = list()
        self.thumbnails: list[dict] = list()
            
    def invoke(self, items: list[ChannelItem], output_folder="backup/ChannelShipper", 
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
    def _extract_details(item: ChannelItem) -> dict:
        """
        extract main details of record
        """
        record = dict()
        # 1. channelId(primary key)
        record['channelId'] = item.channelId

        # 2. snippets(except thumbnails) 
        snippet = item.snippet
        record['title'] = snippet.title
        record['description'] = snippet.description
        record['customUrl'] = snippet.customUrl
        record['publishedAt'] = snippet.publishedAt
        record['country'] = snippet.country

        # 3. statistics
        stats = item.statistics
        record['hiddenSubscriberCount'] = stats.hiddenSubscriberCount
        record['viewCount'] = stats.viewCount
        record['subscriberCount'] = stats.subscriberCount
        record['videoCount'] = stats.videoCount

        return record
    
    @staticmethod
    def _extract_thumbnails(item: ChannelItem) -> list[dict]:
        """
        return a list of dict of thumbnails
        """
        records = list()

        thumbnails = item.snippet.thumbnails
        for tn in thumbnails:
            record = dict()

            # 1. channelId(foreign primary key)
            record['channelId'] = item.channelId

            # 2. thumbnail
            record.update(asdict(tn))
            records.append(record)

        return records