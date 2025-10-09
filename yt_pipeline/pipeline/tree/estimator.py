from typing import Optional
import logging
from anytree import Node as AnyNode, RenderTree

from yt_pipeline.retriever.base import PipeSettings
from yt_pipeline.foreman.base import IterableForeman, UniqueForeman

from yt_pipeline.regulator.estimator import (ChannelsEstimator, VideosEstimator, PlaylistEstimator, SearchEstimator,
                                             PlaylistItemsEstimator, CommentThreadsEstimator)

from yt_pipeline.pipeline.tree import PipelineBlockNode, BranchedPipeline
from yt_pipeline.pipeline.estimator import EstimationReportMetrics, PipelineEstimationStage, PipelineEstimator, PipelineEstimationReport
from yt_pipeline.pipeline.main import Pipeline, reverse_foreman_map, Foreman


from dataclasses import dataclass, field, asdict


@dataclass
class PipelineForemanDetails:
    name: str
    cost_per_call: int
        

@dataclass
class PipelineEstimationStageNode(PipelineEstimationStage):
    links: list['PipelineEstimationStageNode'] = field(default_factory=list)


def stage_node_to_anytree(node: PipelineEstimationStageNode, metrics: EstimationReportMetrics = "quota"):
    """
    Convert PipelineEstimationStageNode tree structure to anytree
    arguments:
        head: PipelineEstimationStageNode
    return:
        anytree.Node
    """
    match metrics:
        case "items":
            metric = f"{node.n_input} -> {node.n_output}"
        case "quota":
            metric = f"{node.quota_usage}"
        case "all":
            metric = f"{node.n_input} -> {node.n_output} | {node.quota_usage}"
            
    name = f"{node.foreman.name} ({metric})"
    anynode = AnyNode(name=name)

    for child in node.links:
        child_anynode = stage_node_to_anytree(child, metrics=metrics)
        child_anynode.parent = anynode

    return anynode


def show_branched_pipeline_estimation_tree(
    head: PipelineEstimationStageNode, 
    metrics: EstimationReportMetrics = "quota"
):
    """
    """
    anyroot = stage_node_to_anytree(head, metrics=metrics)
    for pre, fill, node in RenderTree(anyroot):
        print(f"{pre}{node.name}")
    

@dataclass
class BranchedPipelineEstimationReport:
    overall_cost: int = 0
    head_stage: PipelineEstimationStageNode = None
        
    def to_dict(self):
        return asdict(self)
    
    def display(self, metrics: EstimationReportMetrics = "quota"):
        """
        visualize estimation report
        """
        print("Overall cost:", self.overall_cost)
        print("Tree structure:")
        show_branched_pipeline_estimation_tree(head=self.head_stage, metrics=metrics)


class BranchedPipelineEstimator(PipelineEstimator):
    """
    Estimates total quota cost and I/O volumes for a branched pipeline
    """
    def __init__(self, pipeline: BranchedPipeline):
        super().__init__(pipeline=pipeline)
        self.stage_type = PipelineEstimationStageNode

    def _estimate_block_cost(self, n_items: int, worker_name: str, 
                             settings: Optional[PipeSettings] = None) -> PipelineEstimationStageNode:
        return super()._estimate_block_cost(n_items=n_items, worker_name=worker_name, settings=settings)
    
    def _estimate_stage(self, idx: int, block: PipelineBlockNode, n_items: int, verbose=0):
        return super()._estimate_stage(idx=idx, block=block, n_items=n_items, verbose=verbose)
    
    def _estimate_branch(self, node: PipelineBlockNode, n_items: int, verbose=0):
        input_count = n_items
        stage_node, output_count = self._estimate_stage(idx=0, block=node, n_items=input_count, verbose=verbose)

        for child in node.links:
            input_count = output_count
            child_stage_node = self._estimate_branch(
                node=child, n_items=input_count, 
                verbose=verbose
            )
            stage_node.links.append(child_stage_node)

        return stage_node
    
    def _accumulate_cost(self, stage: PipelineEstimationStageNode) -> int:
        return stage.quota_usage + sum(self._accumulate_cost(ch) for ch in stage.links)

    def estimate(self, verbose=0) -> PipelineEstimationReport:
        stacks = self.pipeline.stacks
        node = stacks.head
        n_items = len(stacks.initial_input)
        
        stage_node = self._estimate_branch(node=node, n_items=n_items)
        overall_cost = self._accumulate_cost(stage=stage_node)
        return BranchedPipelineEstimationReport(overall_cost=overall_cost, head_stage=stage_node)