from typing import Optional, Literal
import logging

from yt_pipeline.retriever.base import PipeSettings
from yt_pipeline.foreman.base import IterableForeman, UniqueForeman

from yt_pipeline.regulator.estimator import (ChannelsEstimator, VideosEstimator, CaptionsEstimator, PlaylistEstimator, 
                                             SearchEstimator, PlaylistItemsEstimator, CommentThreadsEstimator)

from yt_pipeline.pipeline.main import Pipeline, reverse_foreman_map, Foreman, PipelineBlock


from dataclasses import dataclass, field, asdict


@dataclass
class PipelineForemanDetails:
    name: str
    cost_per_call: int
        

@dataclass
class PipelineEstimationStage:
    foreman: PipelineForemanDetails = None
    n_input: int = None
    n_output: int = None
    item_multiplier: int = None
    max_page: int = None
    quota_usage: int = None
    staged_quota_cost: int = None


EstimationReportMetrics = Literal["items", "quota", "all"]
        
@dataclass
class PipelineEstimationReport:
    overall_cost: int = 0
    stages: list[PipelineEstimationStage] = field(default_factory=list)
        
    def to_dict(self):
        return asdict(self)
    
    def display(self, metrics: EstimationReportMetrics = "quota"):
        """
        visualize report
        """
        for stage in self.stages:
            match metrics:
                case "items":
                    metric = f"{stage.n_input} -> {stage.n_output}"
                case "quota":
                    metric = f"{stage.quota_usage}"
                case "all":
                    metric = f"{stage.n_input} -> {stage.n_output} | {stage.quota_usage}"
                case _:
                    raise ValueError(f"invalid metrics type passed. ({EstimationReportMetrics})")
            print(f"{stage.foreman.name} ({metric})")


class PipelineEstimator:
    """
    Estimates total quota cost and I/O volumes for a pipeline
    """
    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline
        self.stage_type = PipelineEstimationStage

    def _estimate_block_cost(self, n_items: int, worker_name: str, 
                             settings: Optional[PipeSettings] = None) -> PipelineEstimationStage:
#         result = dict()
        result = self.stage_type()
        result.n_input = n_items
    
        match worker_name:
            case "channels":
                estimator = ChannelsEstimator()
                result.quota_usage = estimator.estimate(n_items)
                result.n_output = n_items
                
            case "videos":
                estimator = VideosEstimator()
                result.quota_usage = estimator.estimate(n_items)
                result.n_output = n_items
            
            case "captions":
                estimator = CaptionsEstimator()
                result.quota_usage = estimator.estimate(n_items)
                result.n_output = n_items
                
            case "comments":
                estimator = CommentThreadsEstimator()
                result.quota_usage, result.n_output = estimator.estimate(
                    n_items, settings, estimate_output_count=True
                )
                
            case "playlist_items":
                estimator = PlaylistItemsEstimator()
                result.quota_usage, result.n_output = estimator.estimate(
                    n_items, settings, estimate_output_count=True
                )
                
            case "playlists":
                estimator = PlaylistEstimator()
                result.quota_usage, result.n_output = estimator.estimate(
                    n_items, settings, estimate_output_count=True
                )

            case "search":
                estimator = SearchEstimator()
                result.quota_usage, result.n_output = estimator.estimate(
                    n_items, settings, estimate_output_count=True
                )

            case _:
                raise ValueError(f"invalid worker_name {worker_name} passed")
        
        result.foreman = PipelineForemanDetails(name=worker_name, cost_per_call=estimator.cost_per_call)

        if hasattr(estimator, "output_per_page"):
            result.item_multiplier = estimator.output_per_page
        else:
            result.item_multiplier = 1
            
        return result
    
    def _estimate_stage(self, idx: int, block: PipelineBlock, n_items: int, verbose=0):
        foreman = block.foreman

        logging.debug("\nBlock {}: {}".format(idx, block))

        if verbose:
            logging.info("foreman: {}".format(reverse_foreman_map[type(foreman)]))

        kwargs = {"settings": block.pipe_settings} if block.pipe_settings else {}
        stage_result = self._estimate_block_cost(n_items, worker_name=foreman.name, **kwargs)
        stage_result.max_page = block.pipe_settings.max_page if block.pipe_settings else None

        if verbose:
            logging.info(f"{'Estimated input count  :':<25} {n_items}")
            logging.info(f"{'Estimated output count :':<25} {stage_result.n_output}")
            logging.info(f"{'Estimated quota usage  :':<25} {stage_result.quota_usage}")
            
        n_items = stage_result.n_output    
            
        return stage_result, n_items

    def estimate(self, verbose=0) -> PipelineEstimationReport:
        stacks = self.pipeline.stacks
        n_items = len(stacks.initial_input)
        
        report = PipelineEstimationReport()

        for idx, block in enumerate(stacks.blocks):
            stage_result, n_items = self._estimate_stage(idx=idx, block=block, n_items=n_items, verbose=verbose)
            
            report.overall_cost += stage_result.quota_usage
            stage_result.staged_quota_cost = report.overall_cost

            report.stages.append(stage_result)
        
        logging.info(f"{'Overall estimated quota usage :':<25} {report.overall_cost}")

        return report