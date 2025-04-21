"""
Note: this foreman may be removed in the future
"""

from youtube_data_api.retriever import CaptionsRetriever
from youtube_data_api.retriever.captions.params import CaptionsParams

from youtube_data_api.container import CaptionsContainer

from youtube_data_api.shipper import CaptionsShipper


class CaptionsForeman:
    """
    Retrieve caption resource by videoId
    """
    def __init__(self):
        pass

    def invoke(self, videoId: str, developerKey: str, backup=True):
        # 1. retrieve raw items
        params = CaptionsParams(videoId=videoId)
        worker = CaptionsRetriever(params=params, developerKey=developerKey)
        raw_items = worker.invoke(backup=backup)

        # 2. box raw items
        box = CaptionsContainer(raw_items)

        # 3. pack boxes
        shipper = CaptionsShipper()
        shipper.invoke(box.items)
        return shipper