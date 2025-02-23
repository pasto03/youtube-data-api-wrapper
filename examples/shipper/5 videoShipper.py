from youtube_data_api.retriever import VideosRetriever
from youtube_data_api.container import VideosContainer
from youtube_data_api.shipper import VideoShipper

import pandas as pd

# 1. retrieve raw items
df = pd.read_csv("worship channel search result with duration and tags.csv", index_col=None)
videoIds = df.videoId.tolist()
# print(channelIds)

developerKey = open("developerKey", "rb").read().decode()

worker = VideosRetriever(iterable=videoIds[:1000], developerKey=developerKey)
raw_items = worker.invoke()

# 2. box raw items
box = VideosContainer(raw_items)

# 3. pack boxes
shipper = VideoShipper()
shipper.invoke(box.items)
df = pd.DataFrame(shipper.main_records, index=None)
print(df)
df.to_csv("video main records.csv", index=None, encoding="utf-8-sig")