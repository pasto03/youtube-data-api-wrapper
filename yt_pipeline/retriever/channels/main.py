from ..base import UniqueRetriever
from .params import ChannelsParams, ChannelsCheckboxProps
from .pipe import ChannelsPipe


class ChannelsRetriever(UniqueRetriever):
    """
    Retrieve channel details.

    Parameters
    ----------
    iterable : list of str
        A list of channel IDs.
    developerKey : str
        API key obtained from Google Dev Console.
    """
    def __init__(self, iterable: list[str], developerKey: str, max_workers=8, debug=False):
        super().__init__(iterable, developerKey=developerKey, max_workers=max_workers, debug=debug)
        self.pipe = ChannelsPipe
    
    def _create_params(self, chunk):
        chunk = ",".join(chunk)
        return ChannelsParams(ChannelsCheckboxProps().convert(), id=chunk)
    
    def invoke(self, output_folder="backup/ChannelsRetriever", flatten_result=True,
               filename=None, backup=True, backup_when_halted=False, multithread=False):
        return super().invoke(output_folder=output_folder, flatten_result=flatten_result, 
                              filename=filename, backup=backup, backup_when_halted=backup_when_halted,
                              multithread=multithread)