from typing import Type

from yt_pipeline.pipeline.tree import PipelineBlockNode
from yt_pipeline.pipeline import PipelineBlockConstructor
from yt_pipeline.retriever import RetrieverSettings, PipeSettings


class PipelineBlockNodeConstructor(PipelineBlockConstructor):
    def __init__(self, 
                 pipe_settings: PipeSettings = PipeSettings(max_page=1), 
                 retriever_settings: RetrieverSettings = RetrieverSettings()):
        super().__init__(pipe_settings=pipe_settings, retriever_settings=retriever_settings)
        self.block_type = PipelineBlockNode
    
    def construct(self, notation: str) -> 'PipelineBlockNode':
        return super().construct(notation=notation)