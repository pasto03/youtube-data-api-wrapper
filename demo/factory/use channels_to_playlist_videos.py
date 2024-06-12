"""
demo -- use ChannelsToPlaylistItemsFactory to obtain playlist videos of specific channels
"""
import sys_config
from src.factory import ChannelsToPlaylistItemsFactory

import os

this_py_path = os.path.join(os.getcwd(), "demo", "factory")

channelIds = open(f"{this_py_path}\\09-06-2024 00.40.04 channelIds backup.txt").read().split("\n")
factory = ChannelsToPlaylistItemsFactory(channelIds=channelIds[2:3])
recorder = factory.manufacture()
print(recorder.search_df.head(n=10))

recorder.search_df.to_csv(f"{this_py_path}\\search result1.csv", index=None, encoding="utf-8-sig")
recorder.thumbnail_df.to_csv(f"{this_py_path}\\thumbnail result1.csv", index=None, encoding="utf-8-sig")