from dataclasses import dataclass, field
from typing import Optional, Literal

from utils import video_fn

from src.video.props import VideosCheckboxProps
from src.video.params import VideosParams
from src.pipeline.pipe.base import BasePipe


@dataclass
class VideoPipe(BasePipe):
    """
    obtain video details in json of an unique videoId
    """
    retrieval: Literal["unique"] = field(init=False)
    n: int = field(init=False)
    videoId: Optional[str] = None
    partProps: VideosCheckboxProps = VideosCheckboxProps(snippet=True, contentDetails=True, statistics=True)

    def __post_init__(self):
        super().__post_init__()
        self.retrieval = "unique"
        self.n = 1
    
    def _get_response(self, n: int, pageToken=None) -> dict:
        if not self.videoId:
            raise ValueError("The 'videoId' parameter cannot be empty")
        params = VideosParams(
            part=self.partProps.convert(),
            id=self.videoId,
            pageToken=pageToken,
            maxResults=n
        )

        request = video_fn.list(**params.to_dict())
        response = request.execute()
        return response
    
    def _get_all_response(self, **kwargs):
        raise NotImplementedError
    
    def run_pipe(self) -> list[dict]:
        return [self._get_response(n=1)]