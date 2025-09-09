# yt_pipeline

[![PyPI version](https://badge.fury.io/py/yt-pipeline.svg)](https://badge.fury.io/py/yt-pipeline)

A powerful, modular, and extensible toolkit that streamlines YouTube Data API v3 usage—designed with efficiency, scalability, and simplicity in mind. Retrieve, process, and organize YouTube data in seconds, from one-liners to fully customizable pipelines.

---

## Features

- **Simple Querying** — Instantly fetch channels, videos, comments, and more with concise code.
- **Batch & Multithreaded Efficiency** — Get thousands of results while maximizing quota usage.
- **Pipeline Automation** — Chain multiple API calls into one seamless workflow.
- **Extensibility** — Use “Foreman” for smart object grouping; build custom data pipelines tailored to your needs.
- **Fine-grained Control** — Tune API settings, page limits, types, and outputs for YouTube’s versatile endpoints.

---

## Quickstart

Install with:

```bash
pip install yt_pipeline
```

or:
```bash
pip install git+https://github.com/pasto03/youtube-data-api-wrapper.git
```

### Example: Fetch Channel Details in Bulk

```python
from yt_pipeline.retriever import ChannelsRetriever

channel_ids = ["UC_x5XG1OV2P6uZZ5FSM9Ttw", ...]  # replace with your channel IDs
devKey = "YOUR_YOUTUBE_API_KEY"

worker = ChannelsRetriever(iterable=channel_ids, developerKey=devKey, max_workers=16)
results = worker.invoke(multithread=True)
print("Channels fetched:", len(results))
```

---

### Example: Pipeline — From Search to Video Comments

```python
from yt_pipeline.pipeline import Pipeline, PipelineBlock, PipelineStacks
from yt_pipeline.foreman import SearchForeman, VideosForeman, CommentThreadsForeman
from yt_pipeline.retriever import RetrieverSettings, PipeSettings, SearchParamProps, SearchTypeCheckboxProps

stacks = PipelineStacks(
    initial_input=[
        SearchParamProps(q="python tutorial", order="relevance")
    ],
    blocks=[
        PipelineBlock(
            foreman=SearchForeman(types=SearchTypeCheckboxProps(video=True)),
            pipe_settings=PipeSettings(retrieval="all", max_page=1),
            retriever_settings=RetrieverSettings(multithread=True),
            max_workers=8
        ),
        PipelineBlock(
            foreman=VideosForeman(),
            retriever_settings=RetrieverSettings(multithread=True),
            max_workers=8
        ),
        PipelineBlock(
            foreman=CommentThreadsForeman(),
            pipe_settings=PipeSettings(retrieval="all", max_page=3),
            retriever_settings=RetrieverSettings(multithread=True),
            max_workers=8
        )
    ]
)

pipeline = Pipeline(stacks=stacks, developerKey=devKey)
result = pipeline.invoke()
```

---

## Design Overview

- **Retriever:** For single-step/batch data fetching (Channels, Videos, Comments, etc).
- **Foreman:** For organizing and structuring retrieved data into objects or formatted lists.
- **Pipeline:** For multi-step workflows, chaining API queries as a robust, automated data pipeline.

---

## Supported Endpoints

- Search (channels, videos, playlists)
- Channels, Videos, Playlists, PlaylistItems
- Captions, Comments
- And more...

---

## Documentation

- 📖 Full documentation coming soon!  
- For API reference, advanced usage, and extension guides, stay tuned or check the [docs ➔]().

---

## License

MIT License.

---

Contributions and feedback are welcome!  

---
