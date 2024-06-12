from ..base.props import BaseCheckboxProps
from dataclasses import dataclass, asdict


@dataclass
class VideosCheckboxProps(BaseCheckboxProps):
    """
    set any property in this checkbox to true for API to return the specific property
    """
    contentDetails: bool = False
    fileDetails: bool = False
    id: bool = False
    liveStreamingDetails: bool = False
    localizations: bool = False
    player: bool = False
    processingDetails: bool = False
    recordingDetails: bool = False
    snippet: bool = False
    statistics: bool = False
    status: bool = False
    suggestions: bool = False
    topicDetails: bool = False