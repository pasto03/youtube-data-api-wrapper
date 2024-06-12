"""
demo -- obtain playlist by playlistId, channelId or mine
"""
import sys_config
from utils import playlist_items_fn


from src.playlist_items.props import PlaylistItemsCheckboxProps
from src.playlist_items.params import PlaylistItemsFilter, PlaylistItemsParams
from src.playlist_items import PlaylistItemsResponse


params = PlaylistItemsParams(
    part=PlaylistItemsCheckboxProps(contentDetails=True, id=True, snippet=True, status=True).convert(),         
    filter=PlaylistItemsFilter(playlistId="PLEY_M7xVVeAtB_X7p-xZCq26reDKeRBuM")
)

request = playlist_items_fn.list(**params.to_dict())
response = request.execute()


processed_response = PlaylistItemsResponse(response)

print(processed_response.items[0])