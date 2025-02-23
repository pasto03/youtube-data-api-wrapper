from youtube_data_api.retriever import ChannelsRetriever
from youtube_data_api.container import ChannelsContainer
from youtube_data_api.shipper import ChannelShipper

import pandas as pd

# 1. retrieve raw items
channelIds = ["id1", "id2", ...]
worker = ChannelsRetriever(iterable=channelIds, developerKey="YOUR DEV KEY")
raw_items = worker.invoke()

# 2. box raw items
box = ChannelsContainer(raw_items)

# 3. pack boxes
pack = ChannelShipper()
pack.invoke(box.items)
df = pd.DataFrame(pack.main_records)
print(df)
df.to_csv("channel main records.csv", index=None, encoding="utf-8-sig")