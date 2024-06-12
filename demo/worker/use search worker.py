import sys_config

from src.pipeline.worker import SearchWorker


product = SearchWorker(q="赞美之泉", retrieval="custom", n=1, order="relevance", type="playlist")
print(product.search_items)