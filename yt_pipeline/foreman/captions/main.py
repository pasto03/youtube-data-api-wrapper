"""
Note: this foreman may be removed in the future
"""

from yt_pipeline.retriever import CaptionsRetriever, RetrieverSettings
from yt_pipeline.retriever.captions.params import CaptionsParams

from yt_pipeline.container import CaptionsContainer

from yt_pipeline.shipper import CaptionsShipper

from ...foreman.base import BaseForeman


class CaptionsForeman(BaseForeman):
    """
    Retrieve caption resource by videoId
    """
    def __init__(self):
        super().__init__()
        self.retriever = CaptionsRetriever
        self.container = CaptionsContainer
        self.shipper = CaptionsShipper
        self.name = "captions"

    def invoke(self, iterable: list[str], developerKey: str, 
                retriever_settings: RetrieverSettings = RetrieverSettings(output_folder="backup/CaptionsRetriever"),
                backup_shipper=True, max_workers=8, debug=False,
                as_box=False):
        return super().invoke(iterable=iterable, developerKey=developerKey, retriever_settings=retriever_settings,
                              backup_shipper=backup_shipper, max_workers=max_workers, debug=debug, as_box=as_box)