import time
import json
from typing import TypeAlias, Literal, Optional, List, Type
from dataclasses import dataclass, asdict, field

import logging
logging.basicConfig(level=logging.INFO)


from yt_pipeline.retriever.search import SearchParamProps
from yt_pipeline.retriever.base import PipeSettings, RetrieverSettings
from yt_pipeline.retriever.captions import CaptionsParams
from yt_pipeline.container.videos.main import VideoItem
from yt_pipeline.container.search.main import SearchItem
from yt_pipeline.shipper import CommentThreadsShipper
from yt_pipeline.shipper.base import BaseShipper
from yt_pipeline.foreman.base import IterableForeman, UniqueForeman, BaseForeman
from yt_pipeline.foreman import *
from yt_pipeline.regulator.estimator import (ChannelsEstimator, VideosEstimator, CaptionsEstimator, PlaylistEstimator, 
                                             SearchEstimator, PlaylistItemsEstimator, CommentThreadsEstimator)
from yt_pipeline.pipeline.types import PipelineEstimationStage, PipelineForemanDetails, PipelineEstimationReport
from yt_pipeline.pipeline.props import reverse_foreman_map, PipelineBlock

@dataclass
class PipelineProduct:
    title: str = None
    shipper: BaseShipper | CommentThreadsShipper = None


@dataclass
class PipelineExecutionStage(PipelineEstimationStage):
    ...

@dataclass
class PipelineExecutionReport(PipelineEstimationReport):
    ...


class PipelineExecutionRecorder:
    def __init__(self):
        self.report = PipelineExecutionReport()
        self.stage_type = PipelineExecutionStage

    def _estimate_block_cost(self, n_items: int, worker_name: str, 
                             settings: Optional[PipeSettings] = None) -> PipelineExecutionStage:
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

    def record_stage(self, block: PipelineBlock, n_input: int, n_output: int, verbose=0):
        foreman = block.foreman

        if verbose:
            logging.info("foreman: {}".format(reverse_foreman_map[type(foreman)]))

        kwargs = {"settings": block.pipe_settings} if block.pipe_settings else {}
        stage_result = self._estimate_block_cost(n_items=n_input, worker_name=foreman.name, **kwargs)
        stage_result.max_page = block.pipe_settings.max_page if block.pipe_settings else None

        stage_result.n_output = n_output

        if verbose:
            logging.info(f"{'Input count  :':<25} {n_input}")
            logging.info(f"{'Output count :':<25} {stage_result.n_output}")
            logging.info(f"{'Calculated quota usage  :':<25} {stage_result.quota_usage}")
            
        
        # record stage output to report
        self.report.overall_cost += stage_result.quota_usage
        self.report.stages.append(stage_result)