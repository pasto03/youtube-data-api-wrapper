from typing import TypeAlias, Literal

RetrieveMethod: TypeAlias = Literal["head", "custom", "all"]
OrderProps: TypeAlias = Literal["date", "rating", "viewCount", "relevance", "title", "videoCount"]
QueryTypeProps: TypeAlias = Literal["channel", "playlist", "video"]
