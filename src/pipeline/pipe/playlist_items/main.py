from dataclasses import dataclass

from utils import playlist_items_fn
from ..base import BasePipe
from src.playlist_items.props import PlaylistItemsCheckboxProps
from src.playlist_items.params import PlaylistItemsFilter, PlaylistItemsParams


@dataclass
class PlaylistItemsPipe(BasePipe):
    """obtain playlist items metadata given playlistId"""
    partProps: PlaylistItemsCheckboxProps = PlaylistItemsCheckboxProps(contentDetails=True, id=True, snippet=True, status=True)
    playlistId: str = None
    
    def _get_response(self, n, pageToken=None) -> dict:
        if not self.playlistId:
            raise ValueError("The 'playlistId' parameter cannot be empty")
        params = PlaylistItemsParams(
            part=self.partProps.convert(),         
            filter=PlaylistItemsFilter(playlistId=self.playlistId),
            pageToken=pageToken,
            maxResults=n
        )

        request = playlist_items_fn.list(**params.to_dict())
        response = request.execute()
        return response