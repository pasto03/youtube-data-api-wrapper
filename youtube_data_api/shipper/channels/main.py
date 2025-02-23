from dataclasses import asdict

from youtube_data_api.container.channels.main import ChannelItem
from ..base import BaseShipper


class ChannelShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.output_folder = "backup/ChannelShipper"
    
    def invoke(self, items: list[ChannelItem], output_folder=None, backup=True) -> None:
        """
        run the shipper and obtain output
        """
        return super().invoke(items=items, output_folder=output_folder, backup=backup)
    
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