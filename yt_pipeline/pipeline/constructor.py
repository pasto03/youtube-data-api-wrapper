"""
convert pipeline json to Pipeline object
"""
import logging
from copy import deepcopy

from .main import Pipeline, PipelineBlock, PipelineStacks, foreman_map, reverse_foreman_map, available_block_map
from yt_pipeline.foreman import *
from yt_pipeline.foreman.base import UniqueForeman, IterableForeman, BaseForeman
from yt_pipeline.retriever.search import SearchTypeCheckboxProps, SearchParamProps
from yt_pipeline.retriever.captions import CaptionsParams
from yt_pipeline.retriever import RetrieverSettings


class PipelineStacksConstructor:
    def __init__(self): 
        """
        Convert pipeline stack json dict to PipelineStacks object
        """
        self.backup = False
        self.backup_when_halted = False

    def _construct_foreman(self, foreman_name: str, types: list[str]) -> SearchForeman | IterableForeman | UniqueForeman | BaseForeman:
        # construct foreman
        if not isinstance(foreman_name, str):
            raise TypeError("foreman_name should be a string")
        if foreman_name not in foreman_map.keys():
            raise ValueError(f"Foreman '{foreman_name}' is not supported")
        
        if foreman_name == "search":
            if not types:
                raise ValueError("'types' parameter is missing")
            if not isinstance(types, list):
                raise TypeError("types should be a list")
            if not all(isinstance(t, str) for t in types):
                raise TypeError("types should be list[str]")
            foreman = SearchForeman(SearchTypeCheckboxProps(
                channel="channel" in types,
                playlist="playlist" in types,
                video="video" in types,
            ))

        else:
            foreman = foreman_map[foreman_name]()

        return foreman

    def _construct_block(self, block_json: dict):
        foreman_name = block_json["foreman"]
        types = block_json.get("types") # only effective for "search" / SearchForeman
        page = int(block_json.get("page", 0))       # only effective for IterableForeman
        multithread = block_json.get("multithread", False)
        save_output = block_json.get("save_output", False)
        max_workers = block_json.get("max_workers", 16)     # only effective when multithread=True
        backup_shipper = block_json.get("backup_shipper", False)
        debug = block_json.get("debug", False)


        pipe_settings = PipeSettings(retrieval="all", max_page=page) if page else None
        retriever_settings = RetrieverSettings(backup=self.backup, 
                                               backup_when_halted=self.backup_when_halted, 
                                               multithread=multithread)
        
        foreman = self._construct_foreman(foreman_name=foreman_name, types=types)

        return PipelineBlock(
            foreman=foreman,
            pipe_settings=pipe_settings,
            retriever_settings=retriever_settings,
            save_output=save_output,
            backup_shipper=backup_shipper,
            max_workers=max_workers,
            debug=debug
        )
    
    def _validate_blocks(self, blocks: list[dict], verbose=0):
        """
        return None if ok, else raise TypeError
        """
        if not all(isinstance(block, dict) for block in blocks):
            raise TypeError("blocks must be list[dict]")
        
        _blocks = deepcopy(blocks)
        
        block_count = 0
        block = _blocks[block_count]
        foreman_name = block["foreman"]

        while True:
            if block_count + 1 == len(_blocks):
                return 
            
            block_count += 1
            block = _blocks[block_count]
            next_foreman_name = block["foreman"]
            available_next_blocks = available_block_map[foreman_name]

            if verbose:
                logging.info("Current connection: {} -> {}".format(foreman_name, next_foreman_name))
                logging.info("Available next blocks for {}: {}".format(foreman_name, available_next_blocks))

            if next_foreman_name not in available_next_blocks:
                logging.error("{} cannot be connected to {}".format(next_foreman_name, foreman_name))
                raise TypeError("{} cannot be connected to {}".format(next_foreman_name, foreman_name))
            
            foreman_name = next_foreman_name
    
    def invoke(self, stacks_json: dict, verbose=0):
        initial_input_json: list[str] | list[dict] = stacks_json["initial_input"]
        blocks = stacks_json["blocks"]

        self._validate_blocks(blocks=blocks, verbose=verbose)

        first_foreman = blocks[0]["foreman"]

        if not (all(isinstance(i, str) for i in initial_input_json) 
                or all(isinstance(i, dict) for i in initial_input_json)):
            raise TypeError("initial_input should be list[str] | list[dict]")
        
        if isinstance(initial_input_json[0], dict):
            if first_foreman == "search":
                initial_input: list[SearchParamProps] = [SearchParamProps(**item) for item in initial_input_json]
            elif first_foreman == "captions":
                initial_input: list[CaptionsParams] = [CaptionsParams(**item) for item in initial_input_json]
        else:
            initial_input: list[str] = initial_input_json

        backup = stacks_json.get("backup", False)

        stacks = PipelineStacks(
            initial_input=initial_input,
            blocks=[self._construct_block(item) for item in stacks_json["blocks"]],
            backup=backup
        )

        return stacks