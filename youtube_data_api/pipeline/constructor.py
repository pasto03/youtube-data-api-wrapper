"""
convert pipeline json to Pipeline object
"""
from .main import Pipeline, PipelineBlock, PipelineStacks
# from youtube_data_api.pipeline import Pipeline, PipelineBlock, PipelineStacks
from youtube_data_api.foreman import *
from youtube_data_api.foreman.base import UniqueForeman, IterableForeman
from youtube_data_api.retriever.search import SearchTypeCheckboxProps, SearchParamProps

class PipelineConstructor:
    def __init__(self): 
        """
        Convert pipeline json dict to Pipeline object
        """
        self.foreman_map: dict[str, UniqueForeman | IterableForeman] = {
            "videos": VideosForeman,
            "channels": ChannelsForeman,
            "search": SearchForeman,
            "playlists": PlaylistsForeman,
            "playlist_items": PlaylistItemsForeman,
            "comments": CommentThreadsForeman,
            "captions": CaptionsForeman
        }

    def _construct_foreman(self, foreman_json: dict) -> IterableForeman | UniqueForeman:
        foreman_name = foreman_json["name"]
        foreman = self.foreman_map[foreman_name]
        if foreman_name == "search":
            types = foreman_json["types"]
            # print("types:", types)
            foreman = SearchForeman(types=SearchTypeCheckboxProps(**types))
            # print(foreman.types)
        else:
            foreman = foreman()

        return foreman

    def _construct_block(self, block_json: dict):
        # print("_construct_block() block_json:", block_json)
        foreman_json = block_json["foreman"]
        settings = block_json.get("settings")
        settings = PipeSettings(**settings) if settings else None
        block = PipelineBlock(
            foreman=self._construct_foreman(foreman_json),
            settings=settings,
            save_output=block_json["save_output"]
        )
        return block
    
    def _construct_stacks(self, stacks_json: dict):
        # print("stacks_json:", stacks_json)
        initial_input_json: list[str] | list[dict] = stacks_json["initial_input"]
        if isinstance(initial_input_json[0], dict):
            initial_input: list[SearchParamProps] = [SearchParamProps(**item) for item in initial_input_json]
        else:
            initial_input = initial_input_json

        stacks = PipelineStacks(
            initial_input=initial_input,
            blocks=[self._construct_block(item) for item in stacks_json["blocks"]],
            backup=stacks_json["backup"]
        )

        return stacks
    
    def construct_pipeline(self, pipe_json: dict):
        return Pipeline(
            stacks=self._construct_stacks(pipe_json["stacks"]),
            developerKey=""
        )
    