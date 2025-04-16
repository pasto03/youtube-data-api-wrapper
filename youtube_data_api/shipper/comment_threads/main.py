from dataclasses import asdict
from copy import deepcopy

from youtube_data_api.container.comment_threads.main import CommentThreadsItem
from ..base import BaseShipper


class CommentThreadsShipper(BaseShipper):
    def __init__(self):
        super().__init__()
        self.main_records = None    # comment_threads and replies are used to save data instead
        self.comment_threads = list[dict] = list()
        self.replies = dict[str, list] = dict()
        self.output_folder = "backup/CommentThreadsShipper"
    
    def invoke(self, items: list[CommentThreadsItem], output_folder=None, backup=True) -> None:
        """
        run the shipper and obtain output
        """
        # return super().invoke(items=items, output_folder=output_folder, backup=backup)
        for item in items:
            self._extract_details(item)
            
        if backup:
            self._handle_backup(self.comment_threads, suffix=" comment threads", output_folder=output_folder)
            self._handle_backup(self.replies, suffix=" replies", output_folder=output_folder)
    
    def _extract_details(self, item: CommentThreadsItem):
        record = dict()

        record["kind"] = item.kind
        record["etag"] = item.etag
        record["id"] = item.id
        
        # 1. extract snippet
        snippet_item = asdict(item.snippet)
        top_level_comment_item = snippet_item.pop("topLevelComment")

        record.update(snippet_item)

        record.update(self._extract_comment(deepcopy(top_level_comment_item)))

        self.comment_threads.append(record)

        # 2. extract corresponding replies
        replies = item.replies
        if replies:
            comment_replies = replies.comments
            comment_replies_items = asdict(comment_replies)
            # store comment replies of a parent comment id
            self.replies[item.id] = self._extract_comment_replies(deepcopy(comment_replies_items))

    @staticmethod
    def _extract_comment(raw_comment_item: dict) -> dict:
        comment_item = dict()

        author_channel_id_item = raw_comment_item.pop("authorChannelId")
        comment_item.update(raw_comment_item)

        comment_item["authorChannelId"] = author_channel_id_item["value"]

        return deepcopy(comment_item)
    
    def _extract_comment_replies(self, raw_comment_replies: list[dict]) -> list[dict]:
        comment_replies = [self._extract_comment(rep) for rep in raw_comment_replies]
        return deepcopy(comment_replies)
