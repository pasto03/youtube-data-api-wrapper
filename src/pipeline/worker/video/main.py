from dataclasses import dataclass

from src.pipeline.pipe import VideoPipe
from src.video import VideoResponse, VideoItem
from src.base.utils import flatten_chain


@dataclass
class VideoWorker:
    def __init__(self, videoId: str):
        self.responses: dict | list[dict] = VideoPipe(videoId=videoId).run_pipe()
        self.raw_items = [response.get("items") for response in self.responses]
        self.processed_responses: list[VideoResponse] = [VideoResponse(response) for response in self.responses]
        self.video_items: list[VideoItem] = flatten_chain([response.items for response in self.processed_responses])