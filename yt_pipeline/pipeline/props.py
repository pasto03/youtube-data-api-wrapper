from typing import Literal, Optional, List, Type
from dataclasses import dataclass

import logging
logging.basicConfig(level=logging.INFO)

from yt_pipeline.retriever.search import SearchParamProps
from yt_pipeline.retriever.base import PipeSettings, RetrieverSettings
from yt_pipeline.retriever.captions import CaptionsParams
from yt_pipeline.foreman.base import IterableForeman, UniqueForeman, BaseForeman
from yt_pipeline.foreman import *


Foreman = UniqueForeman | IterableForeman | BaseForeman | CaptionsForeman

@dataclass
class PipelineBlock:
    """
    Represents a single block in a data processing pipeline.
    """
    foreman: Foreman = None
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


ForemanName = Literal["videos", "channels", "search", "playlists", "playlist_items", "comments", "captions"]
InitialInputTypes = List[str] | List[SearchParamProps] | List[CaptionsParams]

foreman_map: dict[ForemanName, Type[Foreman]] = {
            "videos": VideosForeman,
            "channels": ChannelsForeman,
            "search": SearchForeman,
            "playlists": PlaylistsForeman,
            "playlist_items": PlaylistItemsForeman,
            "comments": CommentThreadsForeman,
            "captions": CaptionsForeman
}
reverse_foreman_map: dict[Type[Foreman], ForemanName] = {v: k for k, v in foreman_map.items()}

# example: available blocks for videos: videos -> comments | videos -> captions
available_block_map: dict[ForemanName, list[ForemanName]] = {
    "videos": ["comments", "captions"],
    "channels": ["playlists"],
    "search": ["videos", "channels", "playlists"],
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
        "playlists": lambda x: x.id.playlistId
    },
    "playlists": {
        "playlist_items": lambda x: x.id
    },
    "playlist_items": {
        "videos": lambda x: x.contentDetails.videoId
    }
}