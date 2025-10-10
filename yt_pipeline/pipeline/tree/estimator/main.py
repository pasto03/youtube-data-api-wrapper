from __future__ import annotations

from typing import Optional
import logging
from dataclasses import dataclass, field, asdict
from anytree import Node as AnyNode, RenderTree

from yt_pipeline.retriever.base import PipeSettings

from yt_pipeline.pipeline.tree import BranchedPipeline
from yt_pipeline.pipeline.tree.props import PipelineBlockNode
from yt_pipeline.pipeline.estimator import PipelineEstimator
from yt_pipeline.pipeline.tree.estimator.props import EstimationReportMetrics, PipelineEstimationStageNode, PipelineEstimationReport, BranchedPipelineEstimationReport

from yt_pipeline.pipeline.main import Pipeline, reverse_foreman_map, Foreman


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
    
    def _estimate_stage(self, idx: int, block: PipelineBlockNode, n_items: int, verbose=0
                        ) -> tuple[PipelineEstimationStageNode, int]:
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
        
        stage_node = self._estimate_branch(node=node, n_items=n_items, verbose=verbose)
        overall_cost = self._accumulate_cost(stage=stage_node)
        return BranchedPipelineEstimationReport(overall_cost=overall_cost, head_stage=stage_node)