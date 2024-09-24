import os
import time
import json
from tqdm import tqdm

from ...utils import split_list, build_client, dict_to_json, get_current_time
from .settings import PipeSettings
from .pipe import IterablePipe, UniquePipe
from .params import BaseParams


class IterableRetriever:
    def __init__(self, iterable: list[str], developerKey: str, settings=PipeSettings()):
        self.iterable = iterable
        self.client = build_client(developerKey)
        self.pipe_fn = None
        self.pipe = IterablePipe
        self.settings = settings
        
    def _create_params(self, i):
        return BaseParams(part='snippet')
        
    def invoke(self, output_folder="backup/IterableRetriever", 
               filename=None, backup=True) -> list[dict]:
        raw_items = []
        
        count = 0
        total = len(self.iterable)
        width = 3   # width of formatted text
        bar = tqdm(total=total)

        for i in self.iterable:
            params = self._create_params(i)
            # print(params)
            pipe = self.pipe(params, self.pipe_fn, **self.settings.to_dict())
            items = pipe.run_pipe()
#             print(items)
            # filter empty items
            if items:
                raw_items.extend(items)
            
            bar.update()
            count += 1
            bar.set_description("{:^{}s} / {:^{}s} batch(s) retrieved.".format(str(count), width, str(total), width))
                
        bar.close()
        
        if backup:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            if not filename:
                filename = get_current_time() + ".json"
            records = dict_to_json(raw_items)
            with open(os.path.join(output_folder, filename), "wb") as f:
                f.write(records.encode("utf-8"))
        
        return raw_items
    

class UniqueRetriever:
    def __init__(self, iterable: list[str], developerKey: str):
        self.iterable = iterable
        self.chunks = split_list(self.iterable, chunk_size=50)   # split to chunks containing multiple ids
        self.client = build_client(developerKey)
        self.pipe_fn = None
        self.pipe = UniquePipe
    
    def _create_params(self, chunk):
        chunk = ",".join(chunk)
        return BaseParams(part='snippet')
        
    def invoke(self, output_folder="backup/UniqueRetriever", 
               filename=None, backup=True) -> list[dict]:
        raw_items = []
        
        count = 0
        total = len(self.chunks)
        width = 3   # width of formatted text
        bar = tqdm(total=total)

        for chunk in self.chunks:
            params = self._create_params(chunk)
            # print(params)
            pipe = self.pipe(params, self.pipe_fn)
            items = pipe.run_pipe()
#             print(items)
            # filter empty items
            if items:
                raw_items.extend(items)
            
            bar.update()
            count += 1
            bar.set_description("{:^{}s} / {:^{}s} batch(s) retrieved.".format(str(count), width, str(total), width))
                
        bar.close()
        
        if backup:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            if not filename:
                filename = get_current_time() + ".json"
            records = dict_to_json(raw_items)
            with open(os.path.join(output_folder, filename), "wb") as f:
                f.write(records.encode("utf-8"))
        
        return raw_items