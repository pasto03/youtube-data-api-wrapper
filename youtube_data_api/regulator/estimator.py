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
        super().__init__(cost_per_call=1, batch_size=50)


class VideosEstimator(UniqueEstimator):
    def __init__(self):
        super().__init__(cost_per_call=1, batch_size=50)

    
class IterableEstimator(BaseEstimator):
    """
    Any retriever that inherits IterableRetriever:

    If retrieval method == "all":
    - cost = n_items * max_pages * unit_cost

    Else:
    - cost = n_items * unit_cost

    As actual pages is unknown, the actual cost may be lower than estimated cost
    """
    def __init__(self, cost_per_call=1, max_pages=5):
        super().__init__(cost_per_call)
        self.max_pages = max_pages

    def estimate(self, n_items: int, settings: PipeSettings):
        retrieval = settings.retrieval
        pages = self.max_pages if retrieval == "all" else 1
        return n_items * pages * self.cost_per_call
    

class PlaylistItemsEstimator(IterableEstimator):
    def __init__(self, max_pages=5):
        super().__init__(cost_per_call=1, max_pages=max_pages)


class PlaylistEstimator(IterableEstimator):
    def __init__(self, max_pages=5):
        super().__init__(cost_per_call=1, max_pages=max_pages)


class SearchEstimator(IterableEstimator):
    def __init__(self, max_pages=5):
        super().__init__(cost_per_call=100, max_pages=max_pages)


class CommentThreadsEstimator(IterableEstimator):
    def __init__(self, max_pages=5):
        super().__init__(cost_per_call=1, max_pages=max_pages)