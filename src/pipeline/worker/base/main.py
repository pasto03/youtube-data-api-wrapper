from dataclasses import dataclass
from src.base.parser import BaseResponse, BaseItems


@dataclass
class BaseWorker:
    """a base worker object that should be inherited for actual function"""
    responses: list[dict]
    raw_items: list[dict | None]
    processed_responses: list[BaseResponse]
    channel_items : list[BaseItems]