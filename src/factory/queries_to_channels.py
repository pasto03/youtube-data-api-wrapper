from tqdm import tqdm
import logging
import os

from src.recorder import ChannelRecorder
from src.pipeline.worker import SearchWorker
from src.search.channel import SearchChannelItem

from src.search.props import OrderProps


def convert_queries_to_channelIds(queries: list[str]) -> list[str | None]:
    channelIds = []
    total = len(queries)
    n_noResults = 0
    bar = tqdm(queries, desc="convert queries to channelIds...")
    for index, q in enumerate(queries):
        product = SearchWorker(q=q, retrieval="custom", n=1, order="relevance", type="channel")
        item: SearchChannelItem = product.search_items[0]
        if not item:
            bar.set_description(f"query {q} has no result")
            bar.update()
            n_noResults += 1
            ### need to be handled later
            channelIds.append(None)
            continue
        channelIds.append(item.snippet.channelId)
        noresult_desc = f" | {n_noResults} channelId(s) skipped" if n_noResults > 0 else ""
        desc = f"{index+1} / {total} channelIds extracted{noresult_desc}"
        bar.set_description(desc)
        bar.update()
    bar.close()
    return channelIds


from src.channel import ChannelItem
from src.pipeline.worker import ChannelWorker

def fetch_list_channel_details(channelIds: list[str]) -> list[ChannelWorker | None]:
    """fetch channel details by channelId list"""
    products = []
    total = len(channelIds)
    bar = tqdm(channelIds, desc="extract details from channels...")
    for index, channelId in enumerate(channelIds):
        ### handle situation of no channelId obtained
        if not channelId:
            products.append(None)
            continue
        product = ChannelWorker(channelId=channelId)
        products.append(product)
        bar.set_description(f"{index+1} / {total} channel details extracted")
        bar.update()
    bar.close()
    return products


from datetime import datetime

def channelId_backup(channelIds: list[str], backup_path="backups"):
    """save backup of channelId list"""
    dt_string = datetime.now().strftime("%d-%m-%Y %H.%M.%S")
    if not os.path.exists(backup_path):
        os.mkdir(backup_path)
    backup_path = os.path.join(backup_path, f"{dt_string} channelIds backup.txt")
    with open(backup_path, "wb") as f:
        f.write("\n".join(channelIds).encode("utf-8"))
    logging.info(f"channelIds backup has been saved in {backup_path}")


class QueriesToChannelDetailsFactory:
    def __init__(self, queries: list[str]=None, channelIds: list[str]=None, 
                 backup_path="backups", order: OrderProps="relevance"):
        """
        procedure:
        - queries -> channelIds -> Dataframes of channel details
        
        final product: 
        - ChannelRecorder instance with Dataframes of channel details and channel thumbnails

        pass channelIds from backup if applicable; if passed, queries parameters will be ignored
        """
        self.queries = queries
        self.channelIds = channelIds
        self.backup_path = backup_path
        self.order = order

    def _convert_queries_to_channelIds(self) -> list[str | None]:
        channelIds = []
        queries = self.queries
        total = len(queries)
        n_noResults = 0
        bar = tqdm(queries, desc="convert queries to channelIds...")
        for index, q in enumerate(queries):
            product = SearchWorker(q=q, retrieval="custom", n=1, order=self.order, type="channel")
            item: SearchChannelItem = product.search_items[0]
            if not item:
                bar.set_description(f"query {q} has no result")
                bar.update()
                n_noResults += 1
                ### need to be handled later
                channelIds.append(None)
                continue
            channelIds.append(item.snippet.channelId)
            noresult_desc = f" | {n_noResults} channelId(s) skipped" if n_noResults > 0 else ""
            desc = f"{index+1} / {total} channelIds extracted{noresult_desc}"
            bar.set_description(desc)
            bar.update()
        bar.close()
        return channelIds
    
    def manufacture(self) -> ChannelRecorder | None:
        # raise ValueError if:
        # 1. Neither queries or channelIds passed
        # 2. queries or channelIds only contain empty contents
        if (not self.queries and not self.channelIds):
            raise ValueError("Pass either queries or channelIds parameter")
        
        if self.queries:
            if not any(self.queries):
                raise ValueError("Empty values of queries parameter passed")
        
        if self.channelIds:
            if not any(self.channelIds):
                raise ValueError("Empty values of channelIds parameter passed") 

        # queries -> channelIds
        if not self.channelIds:
            self.channelIds = convert_queries_to_channelIds(self.queries)
            channelId_backup(self.channelIds, backup_path=self.backup_path)
            print("Fetch channelId from queries process completed.")
        
        # channelIds -> channel details
        try:
            products = fetch_list_channel_details(self.channelIds)
            logging.info("fetch_list_channel_details process completed.")
            print("fetch_list_channel_details process completed.")
        except Exception as e:
            logging.error("Fetch channel details failed.")
            print("Fetch channel details failed.")
            logging.error(f"Load channelIds in backup before restart 'manufacture' to avoid wastage of quota cost")
            raise e
        
        try:
            recorder = ChannelRecorder(products)
            print("channel details have been recorded to ChannelRecorder.")
        except Exception as e:
            logging.error("ChannelRecorder process failed.")
            logging.error(f"Load backup in the factory before restart 'manufacture' to avoid wastage of quota cost")
            raise e
        return recorder
