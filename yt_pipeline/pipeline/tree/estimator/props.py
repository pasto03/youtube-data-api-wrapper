from __future__ import annotations

import json
from typing import Optional
import logging
from anytree import Node as AnyNode, RenderTree

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
        
    def to_json(self, output_path: str = None) -> None | dict:
        """
        convert object to json (and save to file if output_path specified)
        """
        output = asdict(self)
        if output_path:

            with open(output_path, "wb") as f:
                f.write(json.dumps(output, indent=4, ensure_ascii=False).encode("utf-8"))
        
            logging.info("file saved to {}".format(output_path))
        
        else:
            return output
    
    def display(self, metrics: EstimationReportMetrics = "quota"):
        """
        visualize estimation report
        """
        print("Overall cost:", self.overall_cost)
        print("Tree structure:")
        show_branched_pipeline_estimation_tree(head=self.head_stage, metrics=metrics)
    

@dataclass
class PipelineExecutionStageNode(PipelineEstimationStageNode):
    links: list['PipelineExecutionStageNode'] = field(default_factory=list)


@dataclass
class BranchedPipelineExecutionReport(BranchedPipelineEstimationReport):
    head_stage: PipelineExecutionStageNode = None