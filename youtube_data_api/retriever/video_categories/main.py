from ..base import SingleRetriever
from .pipe import VideoCategoriesPipe
from .params import VideoCategoriesParams


class VideoCategoriesRetriever(SingleRetriever):
    """
    Retrieve YouTube video categories.

    Attributes
    ----------
    pipe_fn : any
        API to obtain response.
    pipe : VideoCategoriesPipe
        Pipe to process request by arguments.

    Parameters
    ----------
    params : list of VideoCategoriesParams
        A list VideoCategoriesParams object as parameter.
    developerKey : str
        API key obtained from Google Dev Console.
    """
    def __init__(self, params: VideoCategoriesParams, developerKey: str):
        super().__init__(params, developerKey)
        self.pipe_fn = self.client.videoCategories()
        self.pipe = VideoCategoriesPipe

    def invoke(self, output_folder="backup/VideoCategoriesRetriever", 
            filename=None, backup=True) -> list[dict]:
        return super().invoke(output_folder=output_folder, filename=filename, backup=backup)