from .params import ChannelsParams

class ChannelsPipe:
    """
    Obtain details of youtube channel(s) by channelId(s).
    Only ChannelsWorker is supposed to implement this object
    """
    def __init__(self, params: ChannelsParams, channel_fn=None):
        self.params = params
        self.channel_fn = channel_fn
        
    def _get_response(self) -> dict:
        if not self.channel_fn:
            raise ValueError("Do not implement this object explicitly. Use ChannelsWorker instead.")
            
        request = self.channel_fn.list(**self.params.to_dict())
        response = request.execute()
        return response
    
    def run_pipe(self) -> list[dict] | None:
        """fetch response from API; if no item fetched, return None"""
        response = self._get_response()
        return response.get("items", None)