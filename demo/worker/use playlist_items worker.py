import sys_config

from src.pipeline.worker import PlaylistItemsWorker


product = PlaylistItemsWorker(playlistId="PLEY_M7xVVeAtB_X7p-xZCq26reDKeRBuM", retrieval="custom", n=3)
print(product.playlist_items)