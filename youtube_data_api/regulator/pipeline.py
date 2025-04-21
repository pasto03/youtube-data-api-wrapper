from typing import Optional, List

from youtube_data_api.retriever.base import PipeSettings
from youtube_data_api.foreman.base import IterableForeman, UniqueForeman
from youtube_data_api.pipeline import Pipeline, PipelineDeliverable

from .estimator import ChannelsEstimator, VideosEstimator, PlaylistEstimator, SearchEstimator, PlaylistItemsEstimator, CommentThreadsEstimator, CaptionsEstimator


class PipelineRegulator:
    HARD_LIMIT = 10000
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

    def _estimate_total_cost(self):
        stacks = self.pipeline.stacks
        n_items = len(stacks.initial_input)

        total_cost = 0

        for idx, block in enumerate(stacks.blocks):
            foreman = block.foreman

            print("\nBlock {}: {}".format(idx, block))
            kwargs = {"settings": block.settings} if block.settings else {}
            result = self._estimate_block_cost(n_items, foreman=foreman, **kwargs)

            if isinstance(result, int):
                cost = result
                # for UniqueForeman, one-to-one relationship exists between input and output
                # n_items = n_items
            else:
                cost, n_items = result
            
            print(f"{'Estimated output count :':<25} {n_items}")
            print(f"{'Estimated quota usage  :':<25} {cost}")

            total_cost += cost

        return total_cost
        
    def invoke(self, bypass_regulation=False, backup=True) -> PipelineDeliverable | None:
        print("---API REGULATOR---")
        # 1. estimate quota cost
        cost = self._estimate_total_cost()

        print("\nEstimated total quota usage: {}.".format(cost))

        if cost > self.HARD_LIMIT and not bypass_regulation:
            print("The request would exceed daily maximum quota cost ({}) if proceed. API call aborted for usage concern. Set bypass_regulation=True to bypass the abortion procedure.".format(self.HARD_LIMIT))

            return
        
        to_proceed = input("Do you want to proceed? (Y/n)")

        if not to_proceed.lower() == "y":
            print("API call aborted.")
            # print("---END OF API REGULATOR---")
        
        else:
            # print("---END OF API REGULATOR---")
            return self.pipeline.invoke()