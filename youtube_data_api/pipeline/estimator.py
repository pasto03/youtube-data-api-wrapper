from typing import Optional

from youtube_data_api.retriever.base import PipeSettings
from youtube_data_api.foreman.base import IterableForeman, UniqueForeman

from youtube_data_api.regulator.estimator import ChannelsEstimator, VideosEstimator, PlaylistEstimator, SearchEstimator, PlaylistItemsEstimator, CommentThreadsEstimator

from .main import Pipeline


class PipelineEstimator:
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

        total_cost = 0

        for idx, block in enumerate(stacks.blocks):
            foreman = block.foreman

            if verbose: print("\nBlock {}: {}".format(idx, block))

            kwargs = {"settings": block.settings} if block.settings else {}
            result = self._estimate_block_cost(n_items, foreman=foreman, **kwargs)

            if verbose: print(f"{'Estimated input count :':<25} {n_items}")

            if isinstance(result, int):
                cost = result
                # for UniqueForeman, one-to-one relationship exists between input and output
                # n_items = n_items
            else:
                cost, n_items = result
            
            if verbose:
                print(f"{'Estimated output count :':<25} {n_items}")
                print(f"{'Estimated quota usage  :':<25} {cost}")

            total_cost += cost

        if verbose: print(f"\n{'Total quota usage :':<25} {total_cost}")

        return total_cost