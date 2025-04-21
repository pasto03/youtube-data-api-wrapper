# youtube-data-api-wrapper

A developer-friendly wrapper for the YouTube Data API v3, designed to simplify video, channel, playlist retrieval and enable pipeline-style data workflows.

---

## 🚀 Quickstart

Retrieve video details given a list of `videoIds`:

```python
from youtube_data_api.foreman import VideosForeman

videoIds = ["id1", "id2", ...]
foreman = VideosForeman()

# Invoke the foreman
shipper = foreman.invoke(iterable=videoIds, developerKey="YOUR_DEV_KEY")

# Access structured output
records = shipper.main_records
thumbnails = shipper.thumbnails
```

All other `Foreman` types follow the same invocation structure.

---

## 🔍 Search with `SearchForeman`

Search for videos, playlists, or channels by keyword:

```python
from youtube_data_api.foreman import SearchForeman
from youtube_data_api.retriever.base import PipeSettings
from youtube_data_api.retriever.search import SearchTypeCheckboxProps, SearchParamProps

# Initialize search types (channel, playlist, video)
foreman = SearchForeman(types=SearchTypeCheckboxProps(channel=True, playlist=True, video=True))

# Run search with custom settings
shipper = foreman.invoke(
    iterable=[SearchParamProps(q="Bruno Mars", order="viewCount")],
    developerKey="YOUR_DEV_KEY",
    settings=PipeSettings(retrieval="all", max_page=5)
)

records = shipper.main_records
```

📄 Complete example: [`examples/foreman/5 SearchForeman.py`](examples/foreman/5%20SearchForeman.py)

---

## 🔧 Build Custom Pipelines

Chain multiple retrieval steps (e.g., search → fetch video details):

```python
def example1():
    from youtube_data_api.pipeline import Pipeline, PipelineBlock, PipelineStacks
    from youtube_data_api.foreman import SearchForeman, VideosForeman
    from youtube_data_api.retriever.base import PipeSettings
    from youtube_data_api.retriever.search import SearchParamProps, SearchTypeCheckboxProps

    blocks = [
        PipelineBlock(
            is_initial=True,
            foreman=SearchForeman(types=SearchTypeCheckboxProps(video=True)),
            settings=PipeSettings(retrieval="head"),
            save_output=True
        ),
        PipelineBlock(
            inputvar_name="videoId",
            foreman=VideosForeman(),
            save_output=True
        )
    ]

    stacks = PipelineStacks(
        initial_input=[SearchParamProps(q="Bruno Mars", order="viewCount")],
        blocks=blocks,
        backup=True
    )

    pipeline = Pipeline(stacks, developerKey="YOUR_DEV_KEY")
    dlv = pipeline.invoke()

    # Save result
    dlv.to_json("OUTPUT.json")
```

📄 Complete example: [`examples/pipeline/example.py`](examples/pipeline/example.py)

---

## 📦 Installation

```bash
pip install git+https://github.com/pasto03/youtube-data-api-wrapper.git
```

(或使用 `pip install .` 安装本地版本)

---

## 📚 Documentation

Coming soon! For now, explore the `examples/` folder for usage references.

---

## 🛠️ Features

- Unified invocation interface for all foreman types
- Dataclass-based inputs and outputs
- Pipeline composition and modularity
- JSON export-ready results

---

## 📜 License

MIT License.

---