import sys_config

from src.pipeline.worker import VideoWorker


product = VideoWorker(videoId="MN13hDmHs54")
print(product.video_items)