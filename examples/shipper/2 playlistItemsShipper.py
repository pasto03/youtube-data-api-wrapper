from youtube_data_api.retriever import PlaylistItemsRetriever
from youtube_data_api.container import PlaylistItemsContainer
from youtube_data_api.shipper import PlaylistItemShipper

import pandas as pd

playlistIds = [
    'PLEY_M7xVVeAtB_X7p-xZCq26reDKeRBuM',
    'PLEY_M7xVVeAsS3Nuf4spTKH1dR3gKvGKz',
    'PLEY_M7xVVeAu-G9MzkZHL7JJydUOft4kd',
    'PLEY_M7xVVeAsxUBE2yYCk16H-oc5iRiXI',
    'PLEY_M7xVVeAtdvFgkcNulGFvQB_dsFoKV'
]

# 1. retrieve raw items
developerKey = open("developerKey", "rb").read().decode()
worker = PlaylistItemsRetriever(iterable=playlistIds, developerKey=developerKey)
items = worker.invoke()


# 2. box raw items
box = PlaylistItemsContainer(items)

# 3. pack boxes
shipper = PlaylistItemShipper()
shipper.invoke(box.items)
df = pd.DataFrame(shipper.main_records)
print(df)
df.to_csv("playlistItems main records.csv", index=None, encoding="utf-8-sig")