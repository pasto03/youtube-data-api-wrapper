from dataclasses import dataclass, asdict
from typing import Optional, Literal, TypeAlias


@dataclass
class CommentThreadsParams:
    part: str = "id,replies,snippet"
    videoId: str = None
    maxResults: int = 20
    moderationStatus: Literal["heldForReview", "likelySpam", "published"] = "published"
    order: Literal["time", "relevance"] = "time"
    pageToken: str = None

    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}