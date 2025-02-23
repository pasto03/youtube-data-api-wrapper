from youtube_data_api.retriever import PlaylistsRetriever
from youtube_data_api.container import PlaylistsContainer
from youtube_data_api.shipper import PlaylistShipper

import pandas as pd


df = pd.read_csv("all channel details.csv", index_col=None)
channelIds = df.channelId.tolist()
# print(channelIds)

# 1. retrieve raw items
developerKey = open("developerKey", "rb").read().decode()

worker = PlaylistsRetriever(iterable=channelIds[:5], developerKey=developerKey)
raw_items = worker.invoke()


# 2. box raw items
box = PlaylistsContainer(raw_items)

# 3. pack boxes
shipper = PlaylistShipper()
shipper.invoke(box.items)
df = pd.DataFrame(shipper.main_records, index=None)
df.to_csv("playlist main records.csv", index=None, encoding="utf-8-sig")