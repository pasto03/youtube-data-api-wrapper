from dataclasses import dataclass, asdict


@dataclass
class BaseParams:   
    """set query parameters here"""
        
    def to_dict(self):
        return {k:v for k, v in asdict(self).items() if v is not None}