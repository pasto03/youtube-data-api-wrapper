import sys_config

from src.pipeline.worker import ChannelPlaylistsWorker


product = ChannelPlaylistsWorker(channelId="UC00EceQGGCMucNvwOS-jQ7A", retrieval="custom", n=1)
print(product.playlist_items)