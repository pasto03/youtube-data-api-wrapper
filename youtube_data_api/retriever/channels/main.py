import os
from tqdm import tqdm

from ...utils import build_client, split_list, dict_to_json, get_current_time
from .params import ChannelsParams, ChannelsCheckboxProps
from .pipe import ChannelsPipe


class ChannelsRetriever:
    def __init__(self, channelId: list[str], developerKey: str):
        self.channelId = channelId
        self.client = build_client(developerKey)
        self.channel_fn = self.client.channels()
    
    def invoke(self, output_folder="backup/ChannelsWorker", filename=None, backup=True, progress_bar=True) -> list[dict]:
        channelId_chunks = split_list(self.channelId, chunk_size=50)
        raw_items = []
        
        count = 0
        total = len(channelId_chunks)
        width = 3
        bar = tqdm(total=total)

        for chunk in channelId_chunks:
            params = ChannelsParams(
                ChannelsCheckboxProps().convert(),
                id=",".join(chunk)
            )
            pipe = ChannelsPipe(params, self.channel_fn)
            items = pipe.run_pipe()
            if items:
                raw_items.extend(items[0].get('items', []))
            
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