from dataclasses import dataclass

from utils import playlists_fn
from src.playlist.props import PlaylistsCheckboxProps
from src.playlist.params import PlaylistsFilter, PlaylistsParams
from src.pipeline.pipe.base import BasePipe

@dataclass
class ChannelPlaylistPipe(BasePipe):
    """obtain playlist items metadata given channelId"""
    channelId: str = None
    
    def _get_response(self, n, pageToken=None) -> dict:
        if not self.channelId:
            raise ValueError("The 'channelId' parameter cannot be empty")
        params = PlaylistsParams(
            part=PlaylistsCheckboxProps(contentDetails=True, snippet=True, status=True).convert(), 
            filter=PlaylistsFilter(channelId=self.channelId),
            pageToken=pageToken,
            maxResults=n
        )

        request = playlists_fn.list(**params.to_dict())
        response = request.execute()
        return response