from src.pipeline.worker import PlaylistItemsWorker
from src.playlist_items.main import PlaylistItemsSnippet, PlaylistItemsContentDetails
from src.common.thumbnail import ItemThumbnail
from src.base.utils import flatten_chain

from pandas.core.frame import DataFrame
import pandas as pd
from tqdm import tqdm
from dataclasses import asdict
from typing import Tuple

class PlaylistItemsRecorder:
    def __init__(self, products: list[PlaylistItemsWorker]):
        self.search_df, self.thumbnail_df = self.record(products)
    
    def record(self, products: list[PlaylistItemsWorker]) -> Tuple[DataFrame |None, DataFrame | None]:
        thumbnail_records = []
        search_records = []
        for product in products:
            ### handle situation of product not produced by a worker
            if not product:
                continue
            for item in product.playlist_items:
                # record search records
                record = self._record_snippet(product.playlistId, item.snippet)
                search_records.append(record)

                # record thumbnails
                thumbnail_records.append(self._record_thumbnails(item.videoId, item.snippet.thumbnails))
            
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
    def _record_snippet(playlistId: str, snippet: PlaylistItemsSnippet) -> dict:
        """extract main snippet data except list or dict value"""
        skip_keys = ["raw_thumbnails", "thumbnails", "position"]
        snippet_record = asdict(snippet)
        filtered_snippet_record = dict()
        filtered_snippet_record['playlistId'] = playlistId
        # switch these columns to top
        filtered_snippet_record['videoId'] = ""
        filtered_snippet_record['playlistId'] = ""
        for k, v in snippet_record.items():
            if k not in skip_keys:
                filtered_snippet_record.update({k:v})
        return filtered_snippet_record
    
    @staticmethod
    def _record_thumbnails(videoId: str, thumbnails: list[ItemThumbnail]) -> list[dict]:
        """convert list of ItemThumbnail object to list of dict"""
        new_thumbnails = list()
        for tn in thumbnails:
            record = {"videoId": videoId}
            record.update(asdict(tn))
            new_thumbnails.append(record)
        return new_thumbnails