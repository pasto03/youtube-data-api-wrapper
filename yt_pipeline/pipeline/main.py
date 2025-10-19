"""
a pipeline with allows muitiple steps of data retrieval
"""
from __future__ import annotations
import time
import json
from typing import TypeAlias, Literal, Optional, List, Type
from dataclasses import dataclass, asdict, field

import logging
logging.basicConfig(level=logging.INFO)


from yt_pipeline.retriever.search import SearchParamProps
from yt_pipeline.retriever.base import PipeSettings, RetrieverSettings
from yt_pipeline.retriever.captions import CaptionsParams
from yt_pipeline.container.videos.main import VideoItem
from yt_pipeline.container.search.main import SearchItem
from yt_pipeline.container import HttpErrorContainer
from yt_pipeline.shipper import CommentThreadsShipper
from yt_pipeline.foreman import *
from yt_pipeline.pipeline.props import Foreman, PipelineBlock, PipelineStacks, ForemanName, InitialInputTypes, foreman_map, reverse_foreman_map, available_block_map, block_access_func_map
from yt_pipeline.pipeline.base.main import PipelineProduct, PipelineExecutionReport, PipelineExecutionRecorder


def validate_connection(parent: Foreman, child: Foreman, verbose=0):
    parent_name = reverse_foreman_map[type(parent)]
    child_name = reverse_foreman_map[type(child)]
    available_next_blocks = available_block_map[parent_name]

    if verbose:
        logging.info("Current connection: {} -> {}".format(parent_name, child_name))
        logging.info("Available next blocks for {}: {}".format(parent_name, available_next_blocks))

    if child_name not in available_next_blocks:
        logging.error("{} cannot be connected to {}".format(child_name, parent_name))
        return False
    
    # when foreman is SearchForeman, if search type does not contain the type needed in next block, return False
    if parent_name == "search" and isinstance(parent, SearchForeman):
        search_types = parent.types

        match child_name:
            # search (videoId)-> videos
            case "videos":
                if not search_types.video:
                    logging.error("missing search type 'video'")
                    return False
                
            # search (channelId)-> channels
            case "channels":
                if not search_types.channel:
                    logging.error("missing search type 'channel'")
                    return False
                
            # search (playlistId)-> playlists
            case "playlists":
                if not search_types.playlist:
                    logging.error("missing search type 'playlist'")
                    return False
                
    return True


@dataclass
class PipelineDeliverable:
    products: List[PipelineProduct] = field(default_factory=list)
    report: PipelineExecutionReport = None

    def to_json(self, output_path: str = None) -> None | dict:
        """
        convert object to json (and save to file if output_path specified)
        """
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

        if output_path:

            with open(output_path, "wb") as f:
                f.write(json.dumps(output, indent=4, ensure_ascii=False).encode("utf-8"))
        
            logging.info("file saved to {}".format(output_path))
        
        else:
            return output


@dataclass
class PipelineErrorContainer:
    """
    container for fatal error
    """
    error_source: ForemanName = None
    error: list[HttpErrorContainer | Exception] = field(default_factory=list)


class Pipeline:
    def __init__(self, stacks: PipelineStacks, developerKey: str):
        self.stacks = stacks
        self.developerKey = developerKey

        self.pipeline_errors = PipelineErrorContainer()

        self._validate_stacks()
    
    def _validate_initial_input(
            self, 
            first_foreman: Foreman,
            initial_input: InitialInputTypes
        ):
        # 1.1 initial_input and blocks must be a list
        if not initial_input or not isinstance(initial_input, list):
            raise TypeError("initial_input must be a list")
    
        # Case 1: foreman = SearchForeman, initial_input must be list[SearchParamProps]
        if isinstance(first_foreman, SearchForeman):
            if not all(isinstance(i, SearchParamProps) for i in initial_input):
                raise TypeError("initial_input should be list[SearchParamProps] when the first foreman is SearchForeman")
        
        # Case 2: foreman = CaptionsForeman, initial_input must be list[CaptionsParams]
        elif isinstance(first_foreman, CaptionsForeman):
            if not all(isinstance(i, CaptionsParams) for i in initial_input):
                raise TypeError("initial_input should be list[CaptionsParams] when the first foreman is CaptionsForeman")

        # Other cases: initial_input must be list[str]
        else:
            if not all(isinstance(i, str) for i in initial_input):
                raise TypeError("initial_input should be list[str]")

    def _validate_stacks(self):
        blocks = self.stacks.blocks
        initial_input = self.stacks.initial_input

        if not isinstance(blocks, list):
            raise TypeError("stacks.blocks must be a list")

        # 1. validate initial input
        self._validate_initial_input(first_foreman=blocks[0].foreman, initial_input=initial_input)
        
        # 2. validate blocks connections
        block_count = 0
        block = blocks[block_count]

        while True:
            if block_count + 1 == len(blocks):
                return
            
            next_block = blocks[block_count + 1]

            if not validate_connection(block.foreman, next_block.foreman):
                raise ValueError("invalid connection")
            
            block = next_block
            block_count += 1

    def __extract_next_input(
            self, items: list, 
            current_foreman_name: ForemanName,
            next_foreman_name: ForemanName
        ) -> list:
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

        return iterable

    def _execute_foreman(
            self, 
            iterable: list,
            foreman: Foreman, 
            pipe_settings: PipeSettings, retriever_settings: RetrieverSettings,
            backup_shipper: bool, max_workers: int, debug: bool
        ):
        kwargs = {"pipe_settings": pipe_settings} if pipe_settings is not None else {}

        try:
            box = foreman.invoke(iterable=iterable, developerKey=self.developerKey, 
            retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
            max_workers=max_workers, debug=debug, as_box=True, **kwargs)
            
            self.pipeline_errors.error_source = reverse_foreman_map[type(foreman)]
            self.pipeline_errors.error = foreman.errors
            return box
        except Exception as e:
            self.pipeline_errors.error_source = reverse_foreman_map[type(foreman)]
            self.pipeline_errors.error = [e]


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
        start = time.time()

        dlv = PipelineDeliverable()
        recorder = PipelineExecutionRecorder()
        dlv.report = recorder.report

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

            box = self._execute_foreman(iterable=iterable, foreman=foreman,
                                        pipe_settings=pipe_settings, retriever_settings=retriever_settings,
                                        backup_shipper=backup_shipper, max_workers=max_workers,
                                        debug=debug)
            
            # Check for fatal errors
            if (not box) or self.pipeline_errors.error:
                logging.error(f"Fatal error occured. Pipeline halted")
                return dlv

            items = box.items
            if not items:
                logging.info("Pipeline early ended due to empty items retrieved. (block: {})".format(block))
                return dlv

            logging.info("{} item(s) retrieved.".format(len(items)))

            # record stage report to report
            recorder.record_stage(block=block, n_input=len(iterable), n_output=len(items))
            
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
            
            # extract iterable for next block
            current_foreman_name = reverse_foreman_map[type(block.foreman)]

            iterable = self.__extract_next_input(items=items, 
                                                 current_foreman_name=current_foreman_name,
                                                 next_foreman_name=next_foreman_name)

            logging.debug("next iterable: {}".format(iterable))

            block_count += 1