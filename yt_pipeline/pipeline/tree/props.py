from __future__ import annotations

import json
import time
import logging
from dataclasses import dataclass, field
from typing import Optional, List

from anytree import Node as AnyNode, RenderTree

from yt_pipeline.pipeline.props import Foreman, InitialInputTypes, PipelineBlock, PipelineStacks, block_access_func_map, reverse_foreman_map, ForemanName
from yt_pipeline.pipeline.main import validate_connection

from yt_pipeline.retriever import PipeSettings, RetrieverSettings

VALIDATE_CONNNECTION_VERBOSE = 0

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

    def _pipeline_to_anytree(self):
        """
        Convert PipelineBlockNode tree structure to anytree
        arguments:
            self: PipelineBlockNode
        return:
            anytree.Node
        """
        # use foreman class name or custom name as node name
        name = getattr(self, "name", None) or type(self.foreman).__name__
        anynode = AnyNode(name=name)

        for child in self.links:
            child_anynode = self._pipeline_to_anytree(child)
            child_anynode.parent = anynode

        return anynode

    def display(self):
        """
        print pipeline tree from current node
        """
        anyroot = self._pipeline_to_anytree(self)
        for pre, fill, node in RenderTree(anyroot):
            print(f"{pre}{node.name}")


@dataclass
class BranchedPipelineStacks(PipelineStacks):
    head: 'PipelineBlockNode' = None