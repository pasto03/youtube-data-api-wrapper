from yt_pipeline.retriever import VideoCategoriesRetriever
from yt_pipeline.retriever.video_categories.params import VideoCategoriesParams

from yt_pipeline.container import VideoCategoriesContainer

from yt_pipeline.shipper import VideoCategoriesShipper


class VideoCategoriesForeman:
    """
    Retrieve video categories by specific region
    """
    def __init__(self):
        pass

    def invoke(self, params: VideoCategoriesParams, developerKey: str, backup=True):
        # 1. retrieve raw items
        worker = VideoCategoriesRetriever(params=params, developerKey=developerKey)
        raw_items = worker.invoke(backup=backup)

        # 2. box raw items
        box = VideoCategoriesContainer(raw_items)

        # 3. pack boxes
        shipper = VideoCategoriesShipper()
        shipper.invoke(box.items)
        return shipper