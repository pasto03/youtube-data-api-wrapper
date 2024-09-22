import os
import time
import json
from tqdm import tqdm


from ...utils import build_client, dict_to_json, get_current_time
from .params import PlaylistsParams, PlaylistsCheckboxProps
from .pipe import PlaylistsPipe


class PlaylistsRetriever:
    def __init__(self, channelIds: list[str], developerKey: str):
        self.channelIds = channelIds
        self.client = build_client(developerKey)
        self.playlist_fn = self.client.playlists()
    
    def invoke(self, output_folder="backup/PlaylistsRetriever", 
               filename=None, backup=True, progress_bar=True) -> list[dict]:
        raw_items = []
        
        count = 0
        total = len(self.channelIds)
        width = 3   # width of formatted text
        bar = tqdm(total=total)

        for channelId in self.channelIds:
            params = PlaylistsParams(
                PlaylistsCheckboxProps().convert(),
                channelId=channelId
            )
#             print(params)
            pipe = PlaylistsPipe(params, self.playlist_fn)
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