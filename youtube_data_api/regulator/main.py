from youtube_data_api.retriever.base import UniqueRetriever, IterableRetriever
from youtube_data_api.regulator.estimator import UniqueEstimator, IterableEstimator, SearchEstimator

class UniqueRegulator:
    HARD_LIMIT = 10000    # any request shall not exceed this quota cost

    def __init__(self, retriever: UniqueRetriever):
        self.retriever = retriever
        self.estimator = UniqueEstimator()

    def _estimate_cost(self) -> int:
        n_items = len(self.retriever.iterable)
        cost = self.estimator.estimate(n_items)
        return cost

    def invoke(self, bypass_regulation=False, backup=True) -> list[dict] | None:
        print("---API REGULATOR---")
        # 1. estimate quota cost
        cost = self._estimate_cost()

        print("Estimated quota usage: {}.".format(cost))

        if cost > self.HARD_LIMIT and not bypass_regulation:
            print("The request would exceed daily maximum quota cost ({}) if proceed. API call aborted for usage concern. Set bypass_regulation=True to bypass the abortion procedure.".format(self.HARD_LIMIT))

            return
        
        to_proceed = input("Do you want to proceed? (Y/n)")

        if not to_proceed.lower() == "y":
            print("API call aborted.")
            # print("---END OF API REGULATOR---")
        
        else:
            # print("---END OF API REGULATOR---")
            return self.retriever.invoke(backup=backup)
     

class ChannelsRegulator(UniqueRegulator):
    def __init__(self, retriever):
        super().__init__(retriever)


class VideosRegulator(UniqueRegulator):
    def __init__(self, retriever):
        super().__init__(retriever)


class IterableRegulator(UniqueRegulator):
    def __init__(self, retriever: IterableRetriever):
        self.retriever = retriever
        self.estimator = IterableEstimator()

    def _estimate_cost(self) -> int:
        n_items = len(self.retriever.iterable)
        settings = self.retriever.settings
        cost = self.estimator.estimate(n_items, settings)
        return cost
    

class PlaylistItemsRegulator(IterableRegulator):
    def __init__(self, retriever):
        super().__init__(retriever)


class PlaylistRegulator(IterableRegulator):
    def __init__(self, retriever):
        super().__init__(retriever)


class SearchRegulator(IterableRegulator):
    def __init__(self, retriever):
        super().__init__(retriever)
        self.estimator = SearchEstimator()


class CommentThreadsRegulator(IterableRegulator):
    def __init__(self, retriever):
        super().__init__(retriever)