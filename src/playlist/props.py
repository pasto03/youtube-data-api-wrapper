from ..base.props import BaseCheckboxProps
from dataclasses import dataclass, asdict


@dataclass
class PlaylistsCheckboxProps(BaseCheckboxProps):
    """
    set any property in this checkbox to true for API to return the specific property
    """
    contentDetails: bool = False
    id: bool = False
    localizations: bool = False
    player: bool = False
    snippet: bool = False
    status: bool = False


