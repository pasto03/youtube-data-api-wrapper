import os
import time
import json
from tqdm import tqdm

from ...utils import build_client, dict_to_json, get_current_time
from .params import PlaylistItemsParams, PlaylistItemsCheckboxProps
from .pipe import PlaylistItemsPipe

class PlaylistItemsRetriever:
    def __init__(self, playlistIds: list[str], developerKey: str):
        self.playlistIds = playlistIds
        self.client = build_client(developerKey)
        self.playlist_items_fn = self.client.playlistItems()
    
    def invoke(self, output_folder="backup/PlaylistItemsRetriever", 
               filename=None, backup=True, progress_bar=True) -> list[dict]:
        raw_items = []
        
        count = 0
        total = len(self.playlistIds)
        width = 3   # width of formatted text
        bar = tqdm(total=total)

        for playlistId in self.playlistIds:
            params = PlaylistItemsParams(
                PlaylistItemsCheckboxProps().convert(),
                playlistId=playlistId
            )
            # print(params)
            pipe = PlaylistItemsPipe(params, self.playlist_items_fn)
            items = pipe.run_pipe()
#             print(items)
            # filter empty items
            if items:
                raw_items.extend(items)
            
            if progress_bar:
                bar.update()
                count += 1
                bar.set_description("{:^{}s} / {:^{}s}".format(str(count), width, str(total), width))
        
        if backup:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            if not filename:
                filename = get_current_time() + ".json"
            records = dict_to_json(raw_items)
            with open(os.path.join(output_folder, filename), "wb") as f:
                f.write(records.encode("utf-8"))
        
        return raw_items