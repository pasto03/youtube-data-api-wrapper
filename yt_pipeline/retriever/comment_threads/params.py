from dataclasses import dataclass, asdict
from typing import Literal, TypeAlias

moderationStatusProps: TypeAlias = Literal["heldForReview", "likelySpam", "published"]
commentThreadOrderProps: TypeAlias = Literal["time", "relevance"]

@dataclass
class CommentThreadParamProps:
    part: str = "id,replies,snippet"
    moderationStatus: moderationStatusProps = "published"
    order: commentThreadOrderProps = "time"
    maxResults: int = 100
    

@dataclass
class CommentThreadsParams:
    part: str = "id,replies,snippet"
    videoId: str = None
    maxResults: int = 100
    moderationStatus: moderationStatusProps = "published"
    order: commentThreadOrderProps = "time"
    # pageToken: str = None

    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}