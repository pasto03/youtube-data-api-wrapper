from src.base.props import BaseCheckboxProps
from dataclasses import dataclass, asdict


@dataclass
class PlaylistItemsCheckboxProps(BaseCheckboxProps):
    """
    set any property in this checkbox to true for API to return the specific property
    """
    contentDetails: bool = False
    id: bool = False
    snippet: bool = False
    status: bool = False