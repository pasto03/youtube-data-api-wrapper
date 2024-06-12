"""
demo -- obtain playlist by playlistId, channelId or mine
"""
import sys_config
from utils import playlists_fn


from src.playlist.props import PlaylistsCheckboxProps
from src.playlist.params import PlaylistsFilter, PlaylistsParams
from src.playlist import PlaylistsResponse


params = PlaylistsParams(
    part=PlaylistsCheckboxProps(contentDetails=True, snippet=True, status=True).convert(), 
    filter=PlaylistsFilter(channelId="UC00EceQGGCMucNvwOS-jQ7A")
)

request = playlists_fn.list(**params.to_dict())
response = request.execute()


processed_response = PlaylistsResponse(response)

print(processed_response.items[0])