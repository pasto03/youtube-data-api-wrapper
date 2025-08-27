from typing import Optional
import logging

from yt_pipeline.retriever.base import PipeSettings
from yt_pipeline.foreman.base import IterableForeman, UniqueForeman

from yt_pipeline.regulator.estimator import ChannelsEstimator, VideosEstimator, PlaylistEstimator, SearchEstimator, PlaylistItemsEstimator, CommentThreadsEstimator

from .main import Pipeline, reverse_foreman_map


class PipelineEstimator:
    """
    Estimates total quota cost and I/O volumes for a pipeline
    """
    # HARD_LIMIT = 10000
    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline

    @staticmethod
    def _estimate_block_cost(n_items: int, foreman: IterableForeman | UniqueForeman, settings: Optional[PipeSettings] = None) -> int | tuple[int, int]:
        worker_name = foreman.name
        match worker_name:
            case "channels":
                return ChannelsEstimator().estimate(n_items)
            case "videos":
                return VideosEstimator().estimate(n_items)
            case "comment_threads":
                return CommentThreadsEstimator().estimate(n_items, settings, estimate_output_count=True)
            case "playlist_items":
                return PlaylistItemsEstimator().estimate(n_items, settings, estimate_output_count=True)
            case "playlists":
                return PlaylistEstimator().estimate(n_items, settings, estimate_output_count=True)
            case "search":
                return SearchEstimator().estimate(n_items, settings, estimate_output_count=True)

    def estimate(self, verbose=0):
        stacks = self.pipeline.stacks
        n_items = len(stacks.initial_input)

        report = dict()
        report['overall_cost'] = 0
        report['stages'] = list()

        total_cost = 0

        for idx, block in enumerate(stacks.blocks):
            stage = dict()

            foreman = block.foreman

            logging.debug("\nBlock {}: {}".format(idx, block))

            if verbose:
                logging.info("foreman: {}".format(reverse_foreman_map[type(foreman)]))
                logging.info("")

            kwargs = {"settings": block.pipe_settings} if block.pipe_settings else {}
            result = self._estimate_block_cost(n_items, foreman=foreman, **kwargs)

            if verbose: logging.info(f"{'Estimated input count  :':<25} {n_items}")
            stage['input_count'] = n_items

            if isinstance(result, int):
                cost = result
                # for UniqueForeman, one-to-one relationship exists between input and output
                # n_items = n_items
            else:
                cost, n_items = result

            if verbose:
                logging.info(f"{'Estimated output count :':<25} {n_items}")
                logging.info(f"{'Estimated quota usage  :':<25} {cost}")

            stage['output_count'] = n_items
            stage['quota_usage'] = cost

            total_cost += cost

            if verbose: logging.info(f"{'Total quota usage :':<25} {total_cost}")

            stage['staged_total_cost'] = total_cost

            report['stages'].append(stage)
        
        logging.info(f"{'Overall estimated quota usage :':<25} {total_cost}")
        report['overall_cost'] = total_cost

        return report