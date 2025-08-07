"""
a pipeline with allows muitiple steps of data retrieval
"""
import time
import json
from typing import Literal, Optional, List, Type
from dataclasses import dataclass, asdict, field

import logging
logging.basicConfig(level=logging.INFO)

from yt_pipeline.retriever.search import SearchParamProps
from yt_pipeline.retriever.base import PipeSettings, RetrieverSettings
from yt_pipeline.retriever.captions import CaptionsParams
from yt_pipeline.container.videos.main import VideoItem
from yt_pipeline.container.search.main import SearchItem
from yt_pipeline.shipper import CommentThreadsShipper
from yt_pipeline.shipper.base import BaseShipper
from yt_pipeline.foreman.base import IterableForeman, UniqueForeman, BaseForeman
from yt_pipeline.foreman import *


@dataclass
class PipelineBlock:
    """
    Represents a single block in a data processing pipeline.
    """
    foreman: IterableForeman | UniqueForeman | BaseForeman = None
    pipe_settings: Optional[PipeSettings] = None
    retriever_settings: RetrieverSettings = None
    save_output: bool = False
    backup_shipper: bool = False
    max_workers: int = 8
    debug: bool = False
    

@dataclass
class PipelineStacks:
    """
    Represents a complete pipeline composed of sequential processing blocks.
    """
    initial_input: List[str] | List[SearchParamProps] | List[CaptionsParams] = None
    blocks: List[PipelineBlock] = None
    backup: bool = False


foreman_map: dict[str, Type[UniqueForeman | IterableForeman | BaseForeman]] = {
            "videos": VideosForeman,
            "channels": ChannelsForeman,
            "search": SearchForeman,
            "playlists": PlaylistsForeman,
            "playlist_items": PlaylistItemsForeman,
            "comments": CommentThreadsForeman,
            "captions": CaptionsForeman
}
reverse_foreman_map: dict[Type[UniqueForeman | IterableForeman | BaseForeman], str] = {v: k for k, v in foreman_map.items()}

# worker = CaptionsForeman()
# print(reverse_foreman_map)
# print(reverse_foreman_map[type(worker)])

# example: available blocks for videos: videos -> comments | videos -> captions
available_block_map = {
    "videos": ["comments", "captions"],
    "channels": ["playlists"],
    "search": ["videos", "channels", "playlists", "playlist_items"],
    "playlists": ["playlist_items"],
    "playlist_items": ["videos"]
}

# function to extract current block output key id as next block input; eg. videos (video["id"]) -> comments
block_access_func_map = {
    "videos": {
        "comments": lambda x: x.id,
        "captions": lambda x: x.id
    },
    "channels": {
        "playlists": lambda x: x.id
    },
    "search": {
        "videos": lambda x: x.id.videoId,
        "channels": lambda x: x.id.channelId,
        "playlists": lambda x: x.id.channelId,
        "playlist_items": lambda x: x.id.playlistId
    },
    "playlists": {
        "playlist_items": lambda x: x.id
    },
    "playlist_items": {
        "videos": lambda x: x.contentDetails.videoId
    }
}


@dataclass
class PipelineProduct:
    title: str = None
    # items: List[dict] = None
    shipper: BaseShipper | CommentThreadsShipper = None


@dataclass
class PipelineDeliverable:
    products: List[PipelineProduct] = field(default_factory=list)

    def to_json(self, output_path: str):
        output = dict()
        output["products"] = list()

        for product in self.products:
            record = dict()
            record["title"] = product.title

            shipper = product.shipper
            shipper_record = dict()
            shipper_record["main_records"] = shipper.main_records
            shipper_record["thumbnails"] = shipper.thumbnails

            if isinstance(shipper, CommentThreadsShipper):
                shipper_record["comment_threads"] = shipper.comment_threads
                shipper_record["replies"] = shipper.replies

            record["shipper"] = shipper_record

            output["products"].append(record)

        with open(output_path, "wb") as f:
            f.write(json.dumps(output, indent=4, ensure_ascii=False).encode("utf-8"))
        
        logging.info("file saved to {}".format(output_path))


class Pipeline:
    def __init__(self, stacks: PipelineStacks, developerKey: str):
        self.stacks = stacks
        self.developerKey = developerKey

    def validate_stacks(self):
        # 1. validate initial input
        blocks = self.stacks.blocks
        initial_input = self.stacks.initial_input

        # 1.1 initial_input must be a list
        if not isinstance(initial_input, list):
            raise TypeError("initial_input must be a list")

        # 1.2 If first foreman is SearchForeman, initial_input must be list[SearchParamProps]
        if isinstance(blocks[0].foreman, SearchForeman):
            if not all(isinstance(i, SearchParamProps) for i in initial_input):
                raise TypeError("initial_input should be list[SearchParamProps] when the first foreman is SearchForeman")
        
        # 1.3 Else, initial_input must be list[str] | list[CaptionsParams]
        else:
            if not all(isinstance(i, (str, CaptionsParams)) for i in initial_input):
                raise TypeError("initial_input must be list[str] | list[CaptionsParams]")
            
        
        # 2. validate blocks connections
        block_count = 0
        block = blocks[block_count]
        foreman_name = reverse_foreman_map[type(block.foreman)]

        while True:
            # foreman_name = reverse_foreman_map[type(block.foreman)]
            if block_count + 1 == len(blocks):
                return True
            
            block_count += 1
            block = blocks[block_count]
            next_foreman_name = reverse_foreman_map[type(block.foreman)]
            available_next_blocks = available_block_map[foreman_name]

            logging.info("Current connection: {} -> {}".format(foreman_name, next_foreman_name))
            logging.info("Available next blocks for {}: {}".format(foreman_name, available_next_blocks))

            if next_foreman_name not in available_next_blocks:
                logging.error("{} cannot be connected to {}".format(next_foreman_name, foreman_name))
                return False
            
            foreman_name = next_foreman_name


    def invoke(self) -> PipelineDeliverable | None:
        """
        Execute the pipeline by processing each block sequentially.

        Execution Steps:
        
        0. Validate stacks: if stacks not valid return
        
        1. Initialize main variables:
            - `dlv` ← `PipelineDeliverable()`
            - `blocks` ← `self.stacks.blocks`
            - `block_count` ← 0
            - `iterable` ← `self.stacks.initial_input`

        2. Loop until return:
            2.1. Get current `PipelineBlock` object:
                - `block` ← `blocks[block_count]`
            
            2.2. Extract keyword parameters from `block`, 
                pass parameters to `foreman` to invoke:
                - `box` ← `foreman.invoke(**kwargs)`

            2.3. Get items from execution:
                - `items` ← `box.items`
                - If no items are retrieved, return.

            2.4. If current block is the last block, return final output:
                - Convert `Container` to `Shipper`:  
                `shipper` ← `foreman._ship(box)`
                - Save to `PipelineProduct`:  
                `product` ← `PipelineProduct(title=block.foreman.name, shipper=shipper)`
                - Append `product` to `dlv.products`
                - Return `dlv`

            2.5. If `save_output` is set to `True` in block, save output:
                - Convert `Container` to `Shipper`:  
                `shipper` ← `foreman._ship(box)`
                - Save to `PipelineProduct`:  
                `product` ← `PipelineProduct(title=block.foreman.name, shipper=shipper)`
                - Append `product` to `dlv.products`

            2.6. Get next block and next foreman's name:
                - `next_block` ← `blocks[block_count + 1]`
                - `next_foreman_name` ← `reverse_foreman_map[type(next_block.foreman)]`

            2.7. Get current foreman's name and extractor function:
                - `current_foreman_name` ← `reverse_foreman_map[type(block.foreman)]`
                - `extractor_function` ← `block_access_func_map[current_foreman_name][next_foreman_name]`

            2.8. Extract ID from `items` as next `iterable`:
                - If `current_foreman_name == "videos"`:  
                `iterable` ← `extract_video_items_id(items: list[VideoItems])`
                - Else if `current_foreman_name == "search"` and `next_foreman_name == "videos"`:  
                `iterable` ← `extract_search_video_items_id(items: list[SearchItems])`
                - Else:  
                `iterable` ← `[extractor_function(i) for i in items]`

            2.9. Increment block count:
                - `block_count += 1`
        """
        is_valid = self.validate_stacks()
        if not is_valid:
            return
        
        start = time.time()

        dlv = PipelineDeliverable()

        blocks: list[PipelineBlock] = self.stacks.blocks
        block_count = 0

        iterable = self.stacks.initial_input

        while True:
            block = blocks[block_count]
            logging.debug("\nBlock {} | block object: {}".format(block_count, block))

            # print("Current iterable: {}\n".format(iterable))

            foreman = block.foreman

            pipe_settings = block.pipe_settings
            retriever_settings = block.retriever_settings
            backup_shipper = block.backup_shipper
            max_workers = block.max_workers
            debug = block.debug

            # print(backup_shipper)

            kwargs = {"pipe_settings": pipe_settings} if pipe_settings is not None else {}

            box = foreman.invoke(iterable=iterable, developerKey=self.developerKey, 
                              retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
                              max_workers=max_workers, debug=debug, as_box=True, **kwargs)

            items = box.items
            if not items:
                logging.info("Pipeline early ended due to empty items retrieved. (block: {})".format(block))
                return
            
            # print("items:", items[:5])

            logging.info("{} item(s) retrieved.".format(len(items)))
            
            # if current block is the last block, return final output
            if block_count + 1  == len(blocks):
                # print("Final items:", box.items)
                # flattened_items = foreman._ship(box).main_records
                shipper = foreman._ship(box)
                product = PipelineProduct(title=block.foreman.name, shipper=shipper)
                dlv.products.append(product)
                logging.info("Pipeline completed.")
                end = time.time()
                logging.info("Execution time: {:.2f}s".format(end-start))
                return dlv
            
            # add to deliverables if specified
            if block.save_output:
                # flattened_items = foreman._ship(box).main_records
                shipper = foreman._ship(box)
                product = PipelineProduct(title=block.foreman.name, shipper=shipper)
                dlv.products.append(product)
            
            next_block = blocks[block_count + 1]
            next_foreman_name = reverse_foreman_map[type(next_block.foreman)]
            
            # print(items[:3])
            # extract iterable for next block
            current_foreman_name = reverse_foreman_map[type(block.foreman)]
            extractor_function = block_access_func_map[current_foreman_name][next_foreman_name]

            # special case for "videos"; to handle the condition where video comment section is disabled
            if current_foreman_name == "videos":
                # print("is videos")
                iterable = list()
                
                items: list[VideoItem]
                for i in items:
                    # null commentCount means comment section is disabled 
                    if i.statistics.commentCount is None:
                        # print(i.id)
                        continue
                    else:
                        iterable.append(i.id)

            # a bug of YouTube Data API even search types specified as "video", "channel" result can occur
            elif current_foreman_name == "search":
                iterable = list()
                items: list[SearchItem]

                logging.debug("inside search condition block")
                logging.debug("next foreman name: {}".format(next_foreman_name))

                if next_foreman_name == "channels":
                    # logging.debug("first item: {}".format(items[0]))
                    for i in items:
                        # print(i.id)
                        if i.id.kind == "youtube#channel":
                            # print(i.id)
                            iterable.append(i.id.channelId)

                elif next_foreman_name == "playlists":
                    for i in items:
                        # print(i.id)
                        if i.id.kind == "youtube#playlist":
                            # print(i.id)
                            iterable.append(i.id.playlistId)

                elif next_foreman_name == "videos":
                    for i in items:
                        # print(i.id)
                        if i.id.kind == "youtube#video":
                            # print(i.id)
                            iterable.append(i.id.videoId)

                else:
                    logging.error("Invalid foreman name passed. This should have been filtered by validate_stacks() unless it is not working properly")
                    raise ValueError("Invalid foreman name '{}' passed".format(next_foreman_name))
                
            else:
                iterable = [extractor_function(i) for i in items]

            logging.debug("next iterable: {}".format(iterable))

            block_count += 1