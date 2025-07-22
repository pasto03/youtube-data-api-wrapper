"""
a pipeline with allows muitiple steps of data retrieval
"""
import time
import json
from typing import Literal, Optional, List
from dataclasses import dataclass, asdict, field


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

    Attributes:
        foreman (IterableForeman | UniqueForeman | BaseForeman):
            The foreman instance responsible for executing this block's task.
        pipe_settings (Optional[PipeSettings]):
            Configuration specific to the foreman. Only applicable for IterableForeman.
        retriever_settings (RetrieverSettings):
            Configuration specific to the corresponding retriever of a foreman.
        save_output (bool): 
            Whether to include this block's output in the final PipelineDeliverable.
        backup_shipper (bool):
            Whether to backup output from shipper.
        max_workers (int):
            Numbers of workers in concurrent pool in multithreading mode.
        debug (bool):
            Whether to print request url of each API request.
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

    Attributes:
        initial_input (List[str] | List[SearchParamProps] | List[CaptionsParams]):
            The input data passed to the first block in the pipeline.
        blocks (List[PipelineBlock]):
            The ordered list of blocks to be executed in the pipeline.
        backup (bool):
            Whether to backup the output from each block's foreman.
    """
    initial_input: List[str] | List[SearchParamProps] | List[CaptionsParams] = None
    blocks: List[PipelineBlock] = None
    backup: bool = True


foreman_map: dict[str, UniqueForeman | IterableForeman | BaseForeman] = {
            "videos": VideosForeman,
            "channels": ChannelsForeman,
            "search": SearchForeman,
            "playlists": PlaylistsForeman,
            "playlist_items": PlaylistItemsForeman,
            "comments": CommentThreadsForeman,
            "captions": CaptionsForeman
}
reverse_foreman_map: dict[UniqueForeman | IterableForeman | BaseForeman, str] = {v: k for k, v in foreman_map.items()}

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


class Pipeline:
    def __init__(self, stacks: PipelineStacks, developerKey: str):
        self.stacks = stacks
        self.developerKey = developerKey

    def invoke(self) -> PipelineDeliverable | None:
        start = time.time()

        dlv = PipelineDeliverable()

        blocks: list[PipelineBlock] = self.stacks.blocks
        block_count = 0

        iterable = self.stacks.initial_input

        while True:
            block = blocks[block_count]
            print("\nBlock {} | block object: {}".format(block_count, block))

            # print("Current iterable: {}\n".format(iterable))

            foreman = block.foreman

            pipe_settings = block.pipe_settings
            retriever_settings = block.retriever_settings
            backup_shipper = block.backup_shipper
            max_workers = block.max_workers
            debug = block.debug

            kwargs = {"pipe_settings": pipe_settings} if pipe_settings is not None else {}

            box = foreman.invoke(iterable=iterable, developerKey=self.developerKey, 
                              retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
                              max_workers=max_workers, debug=debug, as_box=True, **kwargs)

            items = box.items
            if not items:
                print("Pipeline early ended due to empty items retrieved. (block: {})".format(block))
                return
            
            # print("items:", items[:5])

            print("{} item(s) retrieved.".format(len(items)))
            
            # if current block is the last block, return final output
            if block_count + 1  == len(blocks):
                # print("Final items:", box.items)
                # flattened_items = foreman._ship(box).main_records
                shipper = foreman._ship(box)
                product = PipelineProduct(title=block.foreman.name, shipper=shipper)
                dlv.products.append(product)
                print("Pipeline completed.")
                end = time.time()
                print("Execution time: {:.2f}s".format(end-start))
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
            elif current_foreman_name == "search" and next_foreman_name == "videos":
                iterable = list()

                items: list[SearchItem]
                for i in items:
                    # print(i.id)
                    if i.id.kind == "youtube#video":
                        # print(i.id)
                        iterable.append(i.id.videoId)
                
            else:
                iterable = [extractor_function(i) for i in items]

            block_count += 1