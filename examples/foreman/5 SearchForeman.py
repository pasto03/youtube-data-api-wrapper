"""
search video, playlist, channel given query keyword
"""
from youtube_data_api.foreman import SearchForeman
from youtube_data_api.retriever.base import PipeSettings
from youtube_data_api.retriever.search import SearchTypeCheckboxProps, SearchParamProps


foreman = SearchForeman(types=SearchTypeCheckboxProps(channel=True, playlist=True, video=True))

shipper = foreman.invoke(iterable=[SearchParamProps(q="Bruno Mars", order="viewCount")], developerKey="DEVKEY", 
                         settings=PipeSettings(retrieval="all", max_page=5))
records = shipper.main_records