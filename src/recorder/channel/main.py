from src.channel import ChannelItem
from src.channel.main import ChannelSnippet, ChannelItemStatistics
from src.common.thumbnail import ItemThumbnail
from src.pipeline.worker import ChannelWorker
from src.base.utils import flatten_chain
from pandas.core.frame import DataFrame

import pandas as pd
from dataclasses import asdict
from typing import Tuple


class ChannelRecorder:
    def __init__(self, products: list[ChannelWorker]):
        self.search_df, self.thumbnail_df = self.record(products)
    
    def record(self, products: list[ChannelWorker]) -> Tuple[DataFrame |None, DataFrame | None]:
        thumbnail_records = []
        search_records = []
        for product in products:
            ### handle situation of product not produced by a worker
            if not product:
                continue
            if not product.channel_items:
                continue
            for item in product.channel_items:
                if not item:
                    search_records.append(None)
                    thumbnail_records.append(None)
                    continue
                # record search records
                record = self._record_snippet(product.channelId, item.snippet)
                record.update(self._record_statistics(item.statistics))
                search_records.append(record)

                # record thumbnails
                thumbnail_records.append(self._record_thumbnails(product.channelId, item.snippet.thumbnails))
            
        # flatten thumbnail_records
        thumbnail_records = flatten_chain(thumbnail_records)
            
        # convert search records to dataframe
        if search_records:
            search_df = pd.DataFrame(search_records, columns=search_records[0].keys())
        else:
             search_df = None
        
        # convert thumbnail records to dataframe
        if thumbnail_records:
            thumbnail_df = pd.DataFrame(thumbnail_records, columns=thumbnail_records[0].keys())
        else:
            thumbnail_df = None
        
        return search_df, thumbnail_df
    
    @staticmethod
    def _record_snippet(channelId: str, snippet: ChannelSnippet) -> dict:
        """extract main snippet data except list or dict value"""
        skip_keys = ["raw_thumbnails", "thumbnails"]
        snippet_record = asdict(snippet)
        filtered_snippet_record = dict()
        filtered_snippet_record['channelId'] = channelId
        for k, v in snippet_record.items():
            if k not in skip_keys:
                filtered_snippet_record.update({k:v})
        return filtered_snippet_record
    
    @staticmethod
    def _record_statistics(statistics: ChannelItemStatistics) -> dict:
        """convert ChannelItemStatistics to dict"""
        return asdict(statistics)
    
    @staticmethod
    def _record_thumbnails(channelId: str, thumbnails: list[ItemThumbnail]) -> list[dict]:
        """convert list of ItemThumbnail object to list of dict"""
        new_thumbnails = list()
        for tn in thumbnails:
            record = {"channelId": channelId}
            record.update(asdict(tn))
            new_thumbnails.append(record)
        return new_thumbnails