from dataclasses import dataclass, asdict
from copy import deepcopy

from ..base import ItemThumbnail, BaseContainer


@dataclass
class AuthorChannelId:
    value: str = None


@dataclass
class CommentSnippet:
    authorDisplayName: str = None
    authorProfileImageUrl: str = None
    authorChannelUrl: str = None
    authorChannelId: AuthorChannelId = None
    channelId: str = None
    videoId: str = None
    textDisplay: str = None
    textOriginal: str = None
    parentId: str = None
    canRate: bool = None
    viewerRating: str = None
    likeCount: int = None
    moderationStatus: str = None
    publishedAt: str = None
    updatedAt: str = None


@dataclass
class CommentItem:
    kind: str = "youtube#comment"
    etag: str = None
    id: str = None
    snippet: CommentSnippet = None


@dataclass
class CommentThreadsSnippet:
    channelId: str = None
    videoId: str = None
    topLevelComment: CommentItem = None
    canReply: bool = None
    totalReplyCount: int = None
    isPublic: bool = None


@dataclass
class CommentReplies:
    comments: list[CommentItem] = None


@dataclass
class CommentThreadsItem:
    kind: str = "youtube#commentThread"
    etag: str = None
    id: str = None
    snippet: CommentThreadsSnippet = None
    replies: CommentReplies = None


@dataclass
class CommentThreadsContainer(BaseContainer):
    def __init__(self, raw_items: list[dict]):
        super().__init__(raw_items)
        self.raw_items = deepcopy(raw_items)
        self.items: list | list[CommentThreadsItem] = self._extract_item(self.raw_items)
            
    def _extract_item(self, raw_items) -> list | list[CommentThreadsItem]:
        if len(raw_items) == 0:
            return list()
        
        items = list()
        for r in raw_items:
            item = CommentThreadsItem()

            item.etag = r['etag']
            item.id = r['id']

            item.snippet = self._extract_snippet(deepcopy(r["snippet"]))
            item.replies = self._extract_replies(deepcopy(r.get("replies")))

            items.append(item)

        return items

    def _extract_snippet(self, raw_snippet: dict) -> CommentThreadsSnippet:
        top_level_comment_item: dict = raw_snippet.pop("topLevelComment")
        thread_snippet = CommentThreadsSnippet(**raw_snippet)

        top_level_comment = self._extract_comment(deepcopy(top_level_comment_item))

        thread_snippet.topLevelComment = top_level_comment

        return thread_snippet
    
    def _extract_replies(self, raw_replies: dict) -> CommentReplies:
        if not raw_replies:
            return None
        
        replies = CommentReplies()

        reply_comments: list[CommentItem] = list()

        for raw_comment in raw_replies["comments"]:
            reply_comments.append(self._extract_comment(deepcopy(raw_comment)))

        replies.comments = reply_comments

        return replies

    def _extract_comment(self, raw_comment: dict) -> CommentItem:
        comment_snippet_item = raw_comment.pop("snippet")
        comment = CommentItem(**raw_comment)

        author_channel_id_item: dict = comment_snippet_item.pop("authorChannelId")
        author_channel_id = AuthorChannelId(author_channel_id_item["value"])

        comment.snippet = CommentSnippet(**comment_snippet_item, authorChannelId=author_channel_id)

        return comment