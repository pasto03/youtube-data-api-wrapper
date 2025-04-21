"""
Examples to shown how Pipeline works
"""

"""
Example 1: Get video details by searching specific keyword(s)
"""
def example1():
    from youtube_data_api.pipeline import Pipeline, PipelineBlock, PipelineStacks
    from youtube_data_api.foreman import SearchForeman, VideosForeman
    from youtube_data_api.retriever.base import PipeSettings
    from youtube_data_api.retriever.search import SearchParamProps, SearchTypeCheckboxProps

    # always set the is_initial=True for the first block
    # Note: The actual inputvar_name can be determined by checking the output structure of last foreman's container
    blocks = [
        PipelineBlock(is_initial=True, foreman=SearchForeman(types=SearchTypeCheckboxProps(video=True)), settings=PipeSettings(retrieval="head"), save_output=True),
        PipelineBlock(inputvar_name="videoId", foreman=VideosForeman(), save_output=True)
    ]

    stacks = PipelineStacks(initial_input=[SearchParamProps(q="Bruno Mars", order="viewCount")], blocks=blocks, backup=True)

    # initialize pipeline and run
    pipeline = Pipeline(stacks, developerKey="DEVKEY")
    dlv = pipeline.invoke()

    # save to json file
    dlv.to_json("OUTPUT.json")


"""
Example 2: Retrieve comment threads of videos exists in playlists of specific channel
- the 4th block (the one with VideosForeman) effectively remove private or unavailable items (its output filters out unavailable video items)
- PipelineRegulator estimate quota cost for whole pipeline and receive user prompt to determine if proceed to pipeline
"""
def example2():
    from youtube_data_api.pipeline import Pipeline, PipelineBlock, PipelineStacks
    from youtube_data_api.foreman import SearchForeman, PlaylistsForeman, PlaylistItemsForeman, VideosForeman, CommentThreadsForeman
    from youtube_data_api.retriever.base import PipeSettings
    from youtube_data_api.retriever.search import SearchParamProps, SearchTypeCheckboxProps

    from youtube_data_api.regulator import PipelineRegulator


    blocks = [
        PipelineBlock(is_initial=True, foreman=SearchForeman(types=SearchTypeCheckboxProps(channel=True)), settings=PipeSettings(retrieval="custom", n=1), save_output=True),
        PipelineBlock(inputvar_name="channelId", foreman=PlaylistsForeman(), settings=PipeSettings(max_page=2), save_output=True),
        PipelineBlock(inputvar_name="id", foreman=PlaylistItemsForeman(), settings=PipeSettings(max_page=5), save_output=True),
        PipelineBlock(inputvar_name="videoId", foreman=VideosForeman(), save_output=True),
        PipelineBlock(inputvar_name="videoId", foreman=CommentThreadsForeman(), settings=PipeSettings(retrieval="head"), save_output=True)
    ]

    stacks = PipelineStacks(initial_input=[SearchParamProps(q="Elevation Worship", order="relevance")], blocks=blocks)

    pipeline = Pipeline(stacks, developerKey="DEVKEY")
    # dlv = pipeline.invoke()

    regulator = PipelineRegulator(pipeline)
    dlv = regulator.invoke()
    dlv.to_json("PIPELINE_OUTPUT.json")