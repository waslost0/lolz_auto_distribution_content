from entities.entity_util import *
from entities.links import Links
from entities.permission import Permissions


class Post:
    post_id: str
    thread_id: int
    poster_user_id: str
    poster_username: str
    post_create_date: datetime
    post_body: str
    post_body_html: str
    post_body_plain_text: str
    signature: str
    signature_plain_text: str
    post_like_count: int
    post_attachment_count: int
    user_is_ignored: bool
    post_is_published: bool
    post_is_deleted: bool
    post_update_date: datetime
    post_is_first_post: bool
    links: Links
    permissions: Permissions

    def __init__(self, post_id: str, thread_id: int, poster_user_id: str, poster_username: str,
                 post_create_date: datetime,
                 post_body: str, post_body_html: str, post_body_plain_text: str, signature: str,
                 signature_plain_text: str, post_like_count: int, post_attachment_count: int, user_is_ignored: bool,
                 post_is_published: bool, post_is_deleted: bool, post_update_date: datetime, post_is_first_post: bool,
                 links: Links, permissions: Permissions) -> None:
        self.post_id = post_id
        self.thread_id = thread_id
        self.poster_user_id = poster_user_id
        self.poster_username = poster_username
        self.post_create_date = post_create_date
        self.post_body = post_body
        self.post_body_html = post_body_html
        self.post_body_plain_text = post_body_plain_text
        self.signature = signature
        self.signature_plain_text = signature_plain_text
        self.post_like_count = post_like_count
        self.post_attachment_count = post_attachment_count
        self.user_is_ignored = user_is_ignored
        self.post_is_published = post_is_published
        self.post_is_deleted = post_is_deleted
        self.post_update_date = post_update_date
        self.post_is_first_post = post_is_first_post
        self.links = links
        self.permissions = permissions

    @staticmethod
    def from_dict(obj: Any) -> 'Post':
        assert isinstance(obj, dict)
        post_id = str(from_int(obj.get("post_id")))
        thread_id = from_int(obj.get("thread_id"))
        poster_user_id = str(from_int(obj.get("poster_user_id")))
        poster_username = from_str(obj.get("poster_username"))
        post_create_date = from_timestamp(obj.get("post_create_date"))
        post_body = from_str(obj.get("post_body"))
        post_body_html = from_str(obj.get("post_body_html"))
        post_body_plain_text = from_str(obj.get("post_body_plain_text"))
        signature = from_str(obj.get("signature"))
        signature_plain_text = from_str(obj.get("signature_plain_text"))
        post_like_count = from_int(obj.get("post_like_count"))
        post_attachment_count = from_int(obj.get("post_attachment_count"))
        user_is_ignored = from_bool(obj.get("user_is_ignored"))
        post_is_published = from_bool(obj.get("post_is_published"))
        post_is_deleted = from_bool(obj.get("post_is_deleted"))
        post_update_date = from_timestamp(obj.get("post_update_date"))
        post_is_first_post = from_bool(obj.get("post_is_first_post"))
        links = Links.from_dict(obj.get("links"))
        permissions = Permissions.from_dict(obj.get("permissions"))
        return Post(post_id, thread_id, poster_user_id, poster_username, post_create_date, post_body, post_body_html,
                    post_body_plain_text, signature, signature_plain_text, post_like_count, post_attachment_count,
                    user_is_ignored, post_is_published, post_is_deleted, post_update_date, post_is_first_post, links,
                    permissions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["post_id"] = from_int(self.post_id)
        result["thread_id"] = from_int(self.thread_id)
        result["poster_user_id"] = self.poster_user_id
        result["poster_username"] = from_str(self.poster_username)
        result["post_create_date"] = date_to_timestamp(self.post_create_date)
        result["post_body"] = from_str(self.post_body)
        result["post_body_html"] = from_str(self.post_body_html)
        result["post_body_plain_text"] = from_str(self.post_body_plain_text)
        result["signature"] = from_str(self.signature)
        result["signature_plain_text"] = from_str(self.signature_plain_text)
        result["post_like_count"] = from_int(self.post_like_count)
        result["post_attachment_count"] = from_int(self.post_attachment_count)
        result["user_is_ignored"] = from_bool(self.user_is_ignored)
        result["post_is_published"] = from_bool(self.post_is_published)
        result["post_is_deleted"] = from_bool(self.post_is_deleted)
        result["post_update_date"] = date_to_timestamp(self.post_update_date)
        result["post_is_first_post"] = from_bool(self.post_is_first_post)
        result["links"] = to_class(Links, self.links)
        result["permissions"] = to_class(Permissions, self.permissions)
        return result
