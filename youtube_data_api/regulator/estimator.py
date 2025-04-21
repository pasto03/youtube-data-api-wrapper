from dataclasses import dataclass
import math

from youtube_data_api.retriever.captions.params import CaptionsParams
from youtube_data_api.retriever.channels.params import ChannelsParams

from youtube_data_api.retriever.base import PipeSettings


class BaseEstimator:
    def __init__(self, cost_per_call=1):
        self.cost_per_call = cost_per_call

    def estimate(self):
        raise NotImplementedError


class SingleEstimator(BaseEstimator):
    """
    Any retriever that inherits SingleRetriever:
    
    cost = unit_cost
    """
    def __init__(self, cost_per_call=1):
        super().__init__(cost_per_call)

    def estimate(self):
        return self.cost_per_call
    

class CaptionsEstimator(SingleEstimator):
    def __init__(self):
        super().__init__(cost_per_call=50)

    
class VideoCategoriesEstimator(SingleEstimator):
    def __init__(self):
        super().__init__(cost_per_call=1)
    

class UniqueEstimator(BaseEstimator):
    """
    Any retriever that inherits UniqueRetriever:

    cost = n_batch * unit_cost
    """
    def __init__(self, cost_per_call=1, batch_size=50):
        super().__init__(cost_per_call)
        self.batch_size = batch_size

    def estimate(self, n_items: int):
        batch_no = math.ceil(n_items / self.batch_size)
        return batch_no * self.cost_per_call
    

class ChannelsEstimator(UniqueEstimator):
    def __init__(self):
        super().__init__()


class VideosEstimator(UniqueEstimator):
    def __init__(self):
        super().__init__()

    
class IterableEstimator(BaseEstimator):
    """
    Any retriever that inherits IterableRetriever:

    If retrieval method == "all":
    - cost = n_items * max_pages * unit_cost

    Else:
    - cost = n_items * unit_cost

    As actual pages is unknown, the actual cost may be lower than estimated cost
    """
    def __init__(self, cost_per_call=1, output_per_page=50):
        super().__init__(cost_per_call)
        self.output_per_page = output_per_page

    def estimate(self, n_items: int, settings: PipeSettings, estimate_output_count=False) -> int | tuple[int, int]:
        retrieval = settings.retrieval
        max_pages = settings.max_page
        pages = max_pages if retrieval == "all" else 1
        cost = n_items * pages * self.cost_per_call

        print("input_items: {} | pages: {} | cost_per_call: {}".format(n_items, pages, self.cost_per_call))

        if estimate_output_count:
            if retrieval == "custom":
                output_count = settings.n
            else:
                output_count = self.output_per_page * max_pages
            return cost, output_count
        
        return cost
    

class PlaylistItemsEstimator(IterableEstimator):
    def __init__(self):
        super().__init__(cost_per_call=1)


class PlaylistEstimator(IterableEstimator):
    def __init__(self):
        super().__init__(cost_per_call=1)


class SearchEstimator(IterableEstimator):
    def __init__(self):
        super().__init__(cost_per_call=100)


class CommentThreadsEstimator(IterableEstimator):
    def __init__(self):
        super().__init__(cost_per_call=1, output_per_page=100)