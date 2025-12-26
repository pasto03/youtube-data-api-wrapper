# yt_pipeline

[![PyPI version](https://badge.fury.io/py/yt-pipeline.svg)](https://badge.fury.io/py/yt-pipeline)

A powerful, modular, and extensible toolkit that streamlines YouTube Data API v3 usage—designed with efficiency, scalability, and simplicity in mind. Retrieve, process, and organize YouTube data in seconds, from one-liners to fully customizable pipelines.

---

## Features

- **Simple Querying** — Instantly fetch channels, videos, comments, and more with concise code.
- **Batch & Multithreaded Efficiency** — Get thousands of results while maximizing quota usage.
- **Pipeline Automation** — Chain multiple API calls into one seamless workflow (linear or branched/tree-based).
- **String Notation** — Build pipelines using intuitive string syntax for rapid prototyping.
- **Quota Estimation** — Estimate API quota costs before execution to avoid exceeding limits.
- **Execution Reports** — Get detailed metrics on quota usage, execution time, and data flow.
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

### Example: Pipeline with String Notation

```python
from yt_pipeline.pipeline import Pipeline, PipelineStacks, PipelineBlocksConstructor
from yt_pipeline.retriever import RetrieverSettings, PipeSettings, SearchParamProps

devKey = "YOUR_YOUTUBE_API_KEY"

# Build pipeline using string notation
constructor = PipelineBlocksConstructor(
    retriever_settings=RetrieverSettings(multithread=True),
    pipe_settings=PipeSettings(retrieval="all", max_page=1)
)

pipeline_blocks = constructor.construct(
    "search(video)<save_output max_page(1)> -> videos<save_output> -> comments<save_output max_page(2)>"
)

stacks = PipelineStacks(
    initial_input=[SearchParamProps(q="python tutorial")],
    blocks=pipeline_blocks
)

pipeline = Pipeline(stacks=stacks, developerKey=devKey)

# Estimate quota before execution
from yt_pipeline.pipeline import PipelineEstimator
estimator = PipelineEstimator(pipeline)
report = estimator.estimate()
report.display(metrics="all")

# Execute pipeline
result = pipeline.invoke()
```

### Example: Branched Pipeline (Tree Structure)

```python
from yt_pipeline.pipeline.tree import PipelineBlockNodeConstructor, BranchedPipelineStacks, BranchedPipeline
from yt_pipeline.retriever import RetrieverSettings, SearchParamProps

devKey = "YOUR_YOUTUBE_API_KEY"

# Build branched pipeline using string notation
constructor = PipelineBlockNodeConstructor(
    retriever_settings=RetrieverSettings(multithread=True)
)

head = constructor.construct("search(channel,playlist,video)<save_output max_page(1)>")

# Create branches
head.connect("channels<save_output>").connect(
    "playlists<save_output max_page(1)>").connect(
    "playlist_items<save_output>").connect(
    "videos<save_output>"
)

head.connect("playlists<save_output max_page(1)>").connect(
    "playlist_items<save_output>"
)

# Videos branch with comments and captions
videos_head = constructor.construct("videos<save_output>")
videos_head.connect("comments<save_output max_page(1)>")
videos_head.connect("captions<save_output>")
head.connect(videos_head)

# Create and execute branched pipeline
stacks = BranchedPipelineStacks(
    initial_input=[SearchParamProps(q="music")],
    head=head
)

branched_pipeline = BranchedPipeline(stacks=stacks, developerKey=devKey)
result = branched_pipeline.invoke()
```

---

## Design Overview

`yt_pipeline` follows a modular architecture with clear separation of concerns:

### Core Components

- **Retriever** — Directly calls YouTube Data API v3, handles pagination, multithreading, and error handling. Returns raw API responses.

  - `UniqueRetriever`: Batch processing (e.g., multiple channel IDs → channel details)
  - `IterableRetriever`: Paginated results (e.g., channel ID → all playlists)
  - `SingleRetriever`: Single item retrieval (e.g., video ID → captions)

- **Container** — Parses raw API responses into structured dataclass objects for type-safe access.

- **Shipper** — Flattens container objects into dictionaries for easy data export and backup.

- **Foreman** — Orchestrates the complete workflow: `Retriever → Container → Shipper`. Provides a high-level interface for data retrieval and structuring.

- **Pipeline** — Chains multiple Foreman units into automated workflows.

  - `Pipeline`: Linear/sequential pipelines
  - `BranchedPipeline`: Tree-based pipelines with multiple execution paths

- **Regulator** — Estimates quota costs and provides safety checks before API execution.

### Data Flow

```
Input IDs/Params → Retriever → Raw API Response → Container → Structured Objects → Shipper → Flattened Dictionaries
```

In a Pipeline:

```
Initial Input → Foreman₁ → Container₁ → Extract IDs → Foreman₂ → Container₂ → ... → Final Output
```

---

## Supported Endpoints

- Search (channels, videos, playlists)
- Channels, Videos, Playlists, PlaylistItems
- Captions, Comments
- And more...

---

## Documentation

📖 **Comprehensive documentation is available in the [`documentations/`](./documentations/) folder.**

### Quick Links

- **[Component Overview](./documentations/README.md)** — Start here for an overview of all components
- **[Retriever Documentation](./documentations/retriever/retriever.md)** — Direct API calls and data retrieval
- **[Foreman Documentation](./documentations/foreman/foreman.md)** — High-level data orchestration
- **[Pipeline Documentation](./documentations/pipeline/pipeline.md)** — Building automated workflows
- **[Use Cases](./documentations/)** — Practical examples for each component

### Version

Current version: **v1.3.1**

Key features in v1.3.1:

- Branched/tree-based pipelines
- Pipeline quota estimation
- String notation for pipeline construction
- Enhanced execution reports

---

## License

MIT License.

---

Contributions and feedback are welcome!

---
