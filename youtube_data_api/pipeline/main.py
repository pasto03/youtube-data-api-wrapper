from dataclasses import dataclass, field, asdict
from typing import Literal, Optional, List
import json
import time

from youtube_data_api.retriever.search import SearchParamProps
from youtube_data_api.retriever.base import PipeSettings
from youtube_data_api.foreman.base import IterableForeman, UniqueForeman
from youtube_data_api.foreman import CaptionsForeman

from youtube_data_api.container.base import BaseItem
from youtube_data_api.container.search.main import SearchItem
from youtube_data_api.container.playlist_items.main import PlaylistItemsItem



@dataclass
class PipelineBlock:
    """
    Represents a single block in a data processing pipeline.

    Attributes:
        is_initial (bool): Indicates whether this block is the first in the pipeline.
        inputvar_name (Optional[Literal["channelId", "videoId", "playlistId", "id"]]):
            The attribute name of the previous block's output that this block depends on.
        foreman (IterableForeman | UniqueForeman):
            The foreman instance responsible for executing this block's task.
        settings (Optional[PipeSettings]):
            Configuration specific to the foreman. Only applicable for IterableForeman.
        save_output (bool): Whether to include this block's output in the final PipelineDeliverable.
    """
    is_initial: bool = False
    inputvar_name: Optional[Literal["channelId", "videoId", "playlistId", "id"]] = None
    foreman: IterableForeman | UniqueForeman = None
    settings: Optional[PipeSettings] = None
    save_output: bool = False
    

@dataclass
class PipelineStacks:
    """
    Represents a complete pipeline composed of sequential processing blocks.

    Attributes:
        initial_input (List[str] | List[SearchParamProps]):
            The input data passed to the first block in the pipeline.
        blocks (List[PipelineBlock]):
            The ordered list of blocks to be executed in the pipeline.
        backup (bool):
            Whether to backup the output from each block's foreman.
    """
    initial_input: List[str] | List[SearchParamProps] = None
    blocks: List[PipelineBlock] = None
    backup: bool = True


@dataclass
class PipelineProduct:
    title: str = None
    items: List[dict] = None


@dataclass
class PipelineDeliverable:
    products: List[PipelineProduct] = field(default_factory=list)

    def to_json(self, output_path: str):
        with open(output_path, "wb") as f:
            f.write(json.dumps(asdict(self), indent=4, ensure_ascii=False).encode("utf-8"))

class Pipeline:
    def __init__(self, stacks: PipelineStacks, developerKey: str):
        self.stacks = stacks
        self.developerKey = developerKey

    @staticmethod
    def _extract_iterable(items: list[BaseItem], inputvar_name: Literal["channelId", "videoId", "playlistId"] | str):
        # print("inputvar_name:", inputvar_name)
        # print("First item: ", items[0])
        if isinstance(items[0], SearchItem):
            match inputvar_name:
                case "channelId":
                    get_item_id = lambda item: item.id.channelId
                case "videoId":
                    get_item_id = lambda item: item.id.videoId
                case "playlistId":
                    get_item_id = lambda item: item.id.playlistId

            # print("Inside SearchItem extraction.")
            return [get_item_id(item) for item in items]
        
        if isinstance(items[0], PlaylistItemsItem):
            if inputvar_name == "videoId":
                return [item.contentDetails.videoId for item in items]
        
        if not hasattr(items[0], inputvar_name):
            raise AttributeError("Output box items does not contain required input variable of next block. (inputvar_name: {})".format(inputvar_name))
        
        return [getattr(item, inputvar_name) for item in items]

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

            settings = block.settings
            kwargs = {"settings": settings} if settings is not None else {}
            box = foreman.invoke(iterable=iterable, developerKey=self.developerKey, backup=self.stacks.backup, as_box=True, **kwargs)

            items = box.items
            if not items:
                print("Pipeline early ended due to empty items retrieved. (block: {})".format(block))
                return
            
            # iterable = _extract_iterable(box.items, inputvar_name="id")
            # print("DEBUG: iterable:", iterable)

            print("{} item(s) retrieved.".format(len(items)))

            # if block_count == 0:
            #     print("first output items:", items)
            
            # if current block is the last block, return final output
            if block_count + 1  == len(blocks):
                # print("Final items:", box.items)
                flattened_items = foreman._ship(box).main_records
                # print("Final main records: ", flattened_items)
                product = PipelineProduct(title=block.foreman.name, items=flattened_items)
                dlv.products.append(product)
                print("Pipeline completed.")
                end = time.time()
                print("Execution time: {:.2f}s".format(end-start))
                return dlv
            
            # add to deliverables if specified
            if block.save_output:
                flattened_items = foreman._ship(box).main_records
                product = PipelineProduct(title=block.foreman.name, items=flattened_items)
                dlv.products.append(product)
            
            next_block = blocks[block_count + 1]
            assert next_block.inputvar_name, "inputvar_name for the block is not specified. (block: {})".format(next_block)
            
            iterable = self._extract_iterable(items, inputvar_name=next_block.inputvar_name)

            block_count += 1