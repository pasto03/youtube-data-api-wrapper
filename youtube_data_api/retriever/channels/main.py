from ..base import UniqueRetriever
from .params import ChannelsParams, ChannelsCheckboxProps
from .pipe import ChannelsPipe


class ChannelsRetriever(UniqueRetriever):
    """
    Retrieve channel details.

    Attributes
    ----------
    pipe_fn : any
        API to obtain response.
    pipe : ChannelsPipe
        Pipe to process request by arguments.

    Parameters
    ----------
    iterable : list of str
        A list of channel IDs.
    developerKey : str
        API key obtained from Google Dev Console.
    """
    def __init__(self, iterable: list[str], developerKey: str):
        super().__init__(iterable, developerKey)
        self.pipe_fn = self.client.channels()
        self.pipe = ChannelsPipe
    
    def _create_params(self, chunk):
        chunk = ",".join(chunk)
        return ChannelsParams(ChannelsCheckboxProps().convert(), id=chunk)
    
    def invoke(self, output_folder="backup/ChannelsRetriever", 
               filename=None, backup=True) -> list[dict]:
        return super().invoke(output_folder=output_folder, filename=filename, backup=backup)