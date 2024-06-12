from tqdm import tqdm

from src.recorder import PlaylistItemsRecorder
from src.pipeline.worker import ChannelPlaylistsWorker
from src.pipeline.pipe.base import RetrieveMethod
from tqdm import tqdm


# this function is very similar to fetch_list_channel_details()
def fetch_list_channel_playlists(channelIds: list[str], retrieval:RetrieveMethod="all", n=None) -> list[ChannelPlaylistsWorker]:
    """
    fetch channel playlists by channelId list
    
    Note: Do not modify 'retrieval' parameter unless you don't want all results
    """
    products = []
    total = len(channelIds)
    bar = tqdm(channelIds, desc="extract playlists from channels...")
    for index, channelId in enumerate(channelIds):
        product = ChannelPlaylistsWorker(channelId=channelId, retrieval=retrieval, n=n)
        products.append(product)
        bar.set_description(f"{index+1} / {total} channel playlists extracted")
        bar.update()
    bar.close()
    return products


from src.pipeline.worker import PlaylistItemsWorker
from src.pipeline.pipe.base import RetrieveMethod


def fetch_list_playlist_items(playlistIds: list[str], retrieval: RetrieveMethod="all", n=None) -> list[PlaylistItemsWorker | None]:
    """
    fetch playlists items by playlistId list
    
    Note: Do not modify 'retrieval' parameter unless you don't want all results
    """
    products = []
    total = len(playlistIds)
    bar = tqdm(playlistIds, desc="extract playlistItems from playlists...")
    for index, playlistId in enumerate(playlistIds):
        if not playlistId:
            products.append(None)
            continue
        product = PlaylistItemsWorker(playlistId=playlistId, retrieval=retrieval, n=n)
        products.append(product)
        bar.set_description(f"{index+1} / {total} playlists extracted")
        bar.update()
    bar.close()
    return products

    
from src.base.utils import flatten_chain


class ChannelsToPlaylistItemsFactory:
    def __init__(self, channelIds: list[str]):
        """
        procedure:
        - channelIds -> playlists -> playlistItems(similar to videos)
        
        final product: 
        - PlaylistItemsRecorder instance with Dataframes of playlistItem details and playlistItem(video) thumbnails
        """
        self.channelIds = channelIds
    
    def manufacture(self) -> PlaylistItemsRecorder:
        # raise ValueError if empty channelIds is passed
        if not any(self.channelIds):
            raise ValueError("Empty values of channelIds parameter passed") 
        # channelIds -> playlists
        channel_playlist_products = fetch_list_channel_playlists(self.channelIds)
        playlist_items = flatten_chain([product.playlist_items for product in channel_playlist_products])
#         print("{} playlist items present in channel {}".format(len(playlist_items), self.channelIds))
        playlistIds = [item.playlistId for item in playlist_items]
#         print("Fetch playlists from channels process completed.")
        
        # playlists -> playlistItems
        products = fetch_list_playlist_items(playlistIds)
#         logging.info("fetch_list_playlist_items process completed.")
#         print("fetch_list_playlist_items process completed.")
        
        # record to recorder
        recorder = PlaylistItemsRecorder(products)
        print("playlistItems have been recorded to PlaylistItemsRecorder.")
        return recorder