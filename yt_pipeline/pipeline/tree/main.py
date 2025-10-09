from __future__ import annotations

import json
import time
import logging
from dataclasses import dataclass, field
from typing import Optional, List

from anytree import Node as AnyNode, RenderTree

from yt_pipeline.pipeline.main import Foreman, InitialInputTypes, PipelineBlock, PipelineStacks, validate_connection, Pipeline, PipelineProduct, PipelineDeliverable, block_access_func_map, reverse_foreman_map, ForemanName
from yt_pipeline.shipper import CommentThreadsShipper
from yt_pipeline.retriever import PipeSettings, RetrieverSettings, SearchParamProps
from yt_pipeline.retriever.captions.params import CaptionsParams
from yt_pipeline.container.search.main import SearchItem
from yt_pipeline.container.videos.main import VideoItem

VALIDATE_CONNNECTION_VERBOSE = 1


@dataclass
class PipelineBlockNode(PipelineBlock):
    """
    Represents a single block node in a data processing pipeline.
    """
    links: list['PipelineBlockNode'] = field(default_factory=list)
    
    def has_descendant(self, node, target):
        """
        check if target node in parent's descendant
        """
        if not node.links:
            return False
        for child in node.links:
            if child is target:
                return True
            if self.has_descendant(child, target):
                return True
        return False

    def validate_link(self, parent, child):
        """
        validate parent -> child
        Any connection that forms a cycle is not allowed.
        """
        if self.has_descendant(child, parent):
            logging.error(f"Cannot link {child} → {parent}: would create a cycle!")
            return False
        return True

        
    def connect(self, 
                child: 'PipelineBlockNode' | str,
                pipe_settings: Optional[PipeSettings] = PipeSettings(),
                retriever_settings: Optional[RetrieverSettings] = None
                ) -> 'PipelineBlockNode':
        """
        Connect current node with child node provided. 
        
        Child node is returned.
        """
        if isinstance(child, str):
            from .constructor import PipelineBlockNodeConstructor
            # automatically inherit settings from parent node or use default if settings not specified
            pipe_settings = pipe_settings or self.pipe_settings
            retriever_settings = retriever_settings or self.retriever_settings
            constructor = PipelineBlockNodeConstructor(pipe_settings=pipe_settings, retriever_settings=retriever_settings)
            child = constructor.construct(child)

        if not isinstance(child, PipelineBlockNode):
            raise TypeError("invalid child type passed")
        
        # self linked is not allowed
        if child == self:
            logging.error(f"Cannot link with self: would create a cycle!")
            return None
        
        # validate connection
        if not validate_connection(parent=self.foreman, child=child.foreman, verbose=VALIDATE_CONNNECTION_VERBOSE):
            return None
        
        # check if link cycle exists 
        if self.validate_link(parent=self, child=child):  
            self.links.append(child)
            return child
        return None
    
    def remove_links(self):
        """
        remove all links from the current node
        """
        self.links = []

    def display(self):
        """
        print pipeline tree from current node
        """
        return show_pipeline_tree(self)


@dataclass
class BranchedPipelineStacks(PipelineStacks):
    head: 'PipelineBlockNode' = None


def pipeline_to_anytree(head: 'PipelineBlockNode'):
    """
    Convert PipelineBlockNode tree structure to anytree
    arguments:
        head: PipelineBlockNode
    return:
        anytree.Node
    """
    # use foreman class name or custom name as node name
    name = getattr(head, "name", None) or type(head.foreman).__name__
    anynode = AnyNode(name=name)

    for child in head.links:
        child_anynode = pipeline_to_anytree(child)
        child_anynode.parent = anynode

    return anynode


def show_pipeline_tree(head: 'PipelineBlockNode'):
    """
    print pipeline tree
    """
    anyroot = pipeline_to_anytree(head)
    for pre, fill, node in RenderTree(anyroot):
        print(f"{pre}{node.name}")


@dataclass
class PipelineProductNode(PipelineProduct):
    links: list[PipelineProductNode] = field(default_factory=list)


@dataclass
class BranchedPipelineDeliverable:
    head_product: PipelineProductNode = None
        
    def _get_product_record(self, product: PipelineProductNode):
        record = dict()
        record["title"] = product.title

        shipper = product.shipper
        if shipper:
            shipper_record = dict()
            shipper_record["main_records"] = shipper.main_records
            shipper_record["thumbnails"] = shipper.thumbnails

            if isinstance(shipper, CommentThreadsShipper):
                shipper_record["comment_threads"] = shipper.comment_threads
                shipper_record["replies"] = shipper.replies

            record["shipper"] = shipper_record

        return record

    def _get_product(self, node: PipelineProductNode):
        output = self._get_product_record(node)
        child_nodes = node.links

        if child_nodes:
            child_products = list()
            for child_node in child_nodes:
                child_products.append(self._get_product(child_node))
            output["child_products"] = child_products

        return output

    def to_json(self, output_path = None):
        """
        convert object to json (and save to file if output_path specified)
        """
        output = self._get_product(self.head_product)
        
        if output_path:
            with open(output_path, "wb") as f:
                f.write(json.dumps(output, indent=4, ensure_ascii=False).encode("utf-8"))
        
            logging.info("file saved to {}".format(output_path))
        
        else:
            return output
    

class BranchedPipeline(Pipeline):
    def __init__(self, stacks: BranchedPipelineStacks, developerKey: str):
        # super().__init__(stacks=stacks, developerKey=developerKey)
        self.stacks: BranchedPipelineStacks = stacks
        self.developerKey = developerKey

        self._validate_stacks()

    def _validate_initial_input(self, first_foreman: Foreman, initial_input: InitialInputTypes):
        return super()._validate_initial_input(first_foreman=first_foreman, initial_input=initial_input)
    
    def _validate_stacks(self):
        first_foreman = self.stacks.head.foreman
        initial_input = self.stacks.initial_input
        # 1. validate initial input
        self._validate_initial_input(first_foreman=first_foreman, initial_input=initial_input)

        # 2. stacks no need to be validated as it has been validated when initialized
        return
    
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
            backup_shipper: bool, max_workers: int, debug: bool, save_output: bool
        ):
        kwargs = {"pipe_settings": pipe_settings} if pipe_settings is not None else {}

        box = foreman.invoke(iterable=iterable, developerKey=self.developerKey, 
                        retriever_settings=retriever_settings, backup_shipper=backup_shipper, 
                        max_workers=max_workers, debug=debug, as_box=True, **kwargs)
        
        # shipper = foreman._ship(box) if save_output else None
        # return shipper
        return box
    

    def _execute_node(self, node: PipelineBlockNode, iterable: list):
        foreman = node.foreman
        pipe_settings = node.pipe_settings
        retriever_settings = node.retriever_settings
        backup_shipper = node.backup_shipper
        max_workers = node.max_workers
        debug = node.debug

        # print("current_node:", node.foreman.name)

        box = self._execute_foreman(
                iterable=iterable, foreman=foreman,
                pipe_settings=pipe_settings, retriever_settings=retriever_settings, 
                backup_shipper=backup_shipper, max_workers=max_workers, debug=debug, save_output=node.save_output
            )
        
        product = PipelineProductNode(title=node.foreman.name)
        child_products: list[PipelineProductNode] = list()

        child_nodes = node.links
        # print(f"child_nodes: {[i.foreman.name for i in child_nodes]}")

        if child_nodes:
            for child_node in child_nodes:
                # print("current child node:", child_node.foreman.name)
                items = box.items
                logging.info("{} item(s) retrieved.".format(len(items)))

                next_foreman = child_node.foreman
                if items:
                    next_iterable = self.__extract_next_input(
                        items=items, 
                        current_foreman_name=foreman.name, 
                        next_foreman_name=next_foreman.name
                    )
                    if next_iterable:
                        child_products.append(self._execute_node(node=child_node, iterable=next_iterable))
            product.links = child_products

        if node.save_output:
            product.shipper = foreman._ship(box=box)
        return product

    
    def invoke(self) -> BranchedPipelineDeliverable | None:
        """
        """
        start = time.time()

        head_product = self._execute_node(node=self.stacks.head, iterable=self.stacks.initial_input)
        dlv = BranchedPipelineDeliverable(head_product=head_product)

        end = time.time()
        logging.info("Execution time: {:.2f}s".format(end-start))

        return dlv