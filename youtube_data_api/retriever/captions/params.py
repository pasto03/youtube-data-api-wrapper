from dataclasses import dataclass, asdict


@dataclass
class CaptionsParams:
    part: str = "id,snippet"
    videoId: str = None

    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}