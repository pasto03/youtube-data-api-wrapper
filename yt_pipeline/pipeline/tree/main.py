from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional, List

from anytree import Node as AnyNode, RenderTree

from yt_pipeline.pipeline.main import Foreman, PipelineBlock, PipelineStacks, validate_connection, Pipeline
from yt_pipeline.retriever import PipeSettings, RetrieverSettings, SearchParamProps
from yt_pipeline.retriever.captions.params import CaptionsParams


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
                pipe_settings: PipeSettings = PipeSettings(max_page=1), 
                retriever_settings: RetrieverSettings = RetrieverSettings()
                ) -> 'PipelineBlockNode':
        """
        Connect current node with child node provided. 
        
        Child node is returned.
        """
        if isinstance(child, str):
            from .constructor import PipelineBlockNodeConstructor
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


class BranchedPipeline(Pipeline):
    def __init__(self, stacks: BranchedPipelineStacks, developerKey):
        super().__init__(stacks=stacks, developerKey=developerKey)

    def _validate_initial_input(
            self, 
            blocks: List[PipelineBlock],
            initial_input: List[str] | List[SearchParamProps] | List[CaptionsParams]):
        
        raise NotImplementedError()
    
    def _validate_stacks(self):
        pass
        # raise NotImplementedError()
    
    def invoke(self):
        raise NotImplementedError()