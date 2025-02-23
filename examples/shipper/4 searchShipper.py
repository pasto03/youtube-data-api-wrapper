from youtube_data_api.retriever import SearchRetriever
from youtube_data_api.container import SearchContainer
from youtube_data_api.shipper import SearchShipper

import pandas as pd

# 1. retrieve raw items
developerKey = open("developerKey", "rb").read().decode()
worker = SearchRetriever(iterable=["Japanese City Pop"], developerKey=developerKey)
raw_items = worker.invoke(backup=False)


# 2. box raw items
box = SearchContainer(raw_items)

# 3. pack boxes
shipper = SearchShipper()
shipper.invoke(box.items)
df = pd.DataFrame(shipper.main_records, index=None)
print(df)
df.to_csv("search main records.csv", index=None, encoding="utf-8-sig")