import sys_config

from src.pipeline.worker import ChannelWorker


product = ChannelWorker(channelId="UC00EceQGGCMucNvwOS-jQ7A")
print(product.channel_items)