"""
convert pipeline json to Pipeline object
"""
import re
from typing import get_args
import logging
from copy import deepcopy
from dataclasses import replace

from yt_pipeline.retriever.search.params import OrderProps

from .main import Pipeline
from .props import PipelineBlock, PipelineStacks, foreman_map, reverse_foreman_map, available_block_map, ForemanName
from yt_pipeline.foreman import *
from yt_pipeline.foreman.base import UniqueForeman, IterableForeman, BaseForeman
from yt_pipeline.retriever.search import SearchTypeCheckboxProps, SearchParamProps
from yt_pipeline.retriever.captions import CaptionsParams
from yt_pipeline.retriever import RetrieverSettings
from yt_pipeline.retriever.base import PipeSettings


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
        foreman_name: str = block_json["foreman"]
        types = block_json.get("types") # only effective for "search" / SearchForeman
        page = int(block_json.get("page") or 0)    # only effective for IterableForeman; string -> int
        multithread = block_json.get("multithread", False)
        save_output = block_json.get("save_output", False)
        max_workers = block_json.get("max_workers", 16)     # only effective when multithread=True
        backup_shipper = block_json.get("backup_shipper", False)
        debug = block_json.get("debug", False)

        # pipe_settings = PipeSettings(retrieval="all", max_page=page) if page else None
        foreman_class = foreman_map[foreman_name]

        if issubclass(foreman_class, IterableForeman):
            pipe_settings = PipeSettings(retrieval="all", max_page=page)
        else:
            pipe_settings = None

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

        if not (all(isinstance(i, str) for i in initial_input_json) 
            or all(isinstance(i, dict) for i in initial_input_json)):
            raise TypeError("initial_input should be list[str] | list[dict]")
        
        initial_input = list()
        
        if initial_input_json and isinstance(initial_input_json[0], str):
            initial_input: list[str] = initial_input_json
        
        blocks = stacks_json.get("blocks")
        constructed_blocks = None

        if blocks:
            self._validate_blocks(blocks=blocks, verbose=verbose)

            first_foreman = blocks[0]["foreman"]

            if initial_input_json and isinstance(initial_input_json[0], dict):
                if first_foreman == "search":
                    initial_input: list[SearchParamProps] = [SearchParamProps(**item) for item in initial_input_json]
                elif first_foreman == "captions":
                    initial_input: list[CaptionsParams] = [CaptionsParams(**item) for item in initial_input_json]

            backup = stacks_json.get("backup", False)
            constructed_blocks = [self._construct_block(item) for item in blocks]

        stacks = PipelineStacks(
            initial_input=initial_input,
            blocks=constructed_blocks,
            backup=backup
        )

        return stacks


class PipelineBlockConstructor:
    def __init__(self, 
                 pipe_settings: PipeSettings = PipeSettings(max_page=1), 
                 retriever_settings: RetrieverSettings = RetrieverSettings()):
        self.pipe_settings = pipe_settings
        self.retriever_settings = retriever_settings
        self.block_type = PipelineBlock

    def construct(self, notation: str) -> PipelineBlock:
        """
        `<foreman_name><modifier>?` to add modifiers
        - modifier(<save_output | max_workers | max_page>): 
            - save_output: set the parameter as true. Example: `videos<save_output>`
            - max_workers(n), max_page(n): set parameter a value. Example: `channels<max_workers(8)>`, `playlists(max_page(5))`
        
        For SearchForeman, use `search(<types>)` to pass types parameters; available types are `video`, `channel`, `playlist`
        - Example: `search(video,channel,playlist)<save_output>`
        """
        notation = notation.strip()
        modifier = re.findall(r'\<(.*?)\>', notation)
        
        if modifier:
            notation = notation.replace(f"<{modifier[0]}>", "")

        if "search" in notation:
            search_types: list[str] | None = re.findall(r'\((.*?)\)', notation)
            if not search_types:
                raise ValueError("search types not indicated")
            search_types = search_types[0]
            notation = notation.replace(f"({search_types})", "")
            search_types = [i.strip() for i in search_types.split(",")]
            
            # every listed search types must match available search types
            if not set(search_types) <= {"channel", "playlist", "video"}:
                raise ValueError("Invalid search types passed. Only 'channel', 'playlist', or 'video' allowed.")
            
            block = self.block_type(
                foreman=SearchForeman(
                    types=SearchTypeCheckboxProps(**{search_type: True for search_type in search_types})
                ),
                pipe_settings=self.pipe_settings,
                retriever_settings=self.retriever_settings,
            )
        else:
            if not notation in get_args(ForemanName):
                raise ValueError(f"'{notation}' is not in {ForemanName}")
            pipe_settings = self.pipe_settings if notation in ["playlists", "playlist_items", "comments"] else None
            block = self.block_type(
                foreman=foreman_map[notation](),
                pipe_settings=pipe_settings,
                retriever_settings=self.retriever_settings,
            )
        
        if modifier:
            args = modifier[0].split(" ")
            max_page_specified = False
            n_specified = False
            for arg in args:
                if arg == "save_output":
                    block.save_output = True
                    continue
                if "max_workers" in arg:
                    max_workers = re.findall(r'\((.*?)\)', arg)
                    if not max_workers:
                        raise ValueError('max_workers number should be specified with max_workers(n)')
                    block.max_workers = int(max_workers[0])
                elif notation in ["search", "playlists", "playlist_items", "comments"]:
                    # do not allow max_page and n to be specified together
                    if "max_page" in arg:
                        if n_specified:
                            raise ValueError("max_page and n cannot be specified together")
                        max_page = re.findall(r'\((.*?)\)', arg)
                        if not max_page:
                            raise ValueError('max_page number should be specified with max_page(n)')
                        block.pipe_settings = PipeSettings(max_page=int(max_page[0]))
                        max_page_specified = True
                    elif arg.startswith("n("):
                        if max_page_specified:
                            raise ValueError("max_page and n cannot be specified together")
                        n = re.findall(r'\((.*?)\)', arg)
                        if not n:
                            raise ValueError('n number should be specified with n(n)')
                        block.pipe_settings = PipeSettings(n=int(n[0]), retrieval="custom")
                        n_specified = True
                else:
                    raise ValueError(f"invalid modifier argument '{arg}' passed")
                
        return block


class PipelineBlocksConstructor:
    """
    Create pipeline block connections with string declarations
    """
    def __init__(self, 
                 pipe_settings: PipeSettings = PipeSettings(max_page=1), 
                 retriever_settings: RetrieverSettings = RetrieverSettings()):
        self.pipe_settings = pipe_settings
        self.retriever_settings = retriever_settings
        
    def construct(self, notation: str) -> list[PipelineBlock]:
        """
        ### Syntax
        1. `<foreman_name> -> <foreman_name> -> ...` for normal block connections
        - Example: `search -> channels -> playlists -> playlist_items`
        2. `search(<search_types>)? -> <foreman_name> -> ...` to indicate search type
        - search_types: "channel", "playlist", "video"
        - Example: `search(channel,playlist) -> channels -> ...`
        3. `<foreman_name> -> <foreman_name><modifier>? -> ...` to add modifiers
        - modifier(<save_output | max_workers | max_page>): save_output to set the parameter as true, max_workers(n) and max_page(n) to set parameter a value
        - Example: `search -> channels<save_output max_workers(8)> -> playlists` 
        """
        blocks: list[PipelineBlock] = []

        block_constructor = PipelineBlockConstructor(
            pipe_settings=self.pipe_settings, 
            retriever_settings=self.retriever_settings
        )
            
        for n in notation.strip().split("->"):
            block = block_constructor.construct(notation=n)
            blocks.append(block)
        
        return blocks