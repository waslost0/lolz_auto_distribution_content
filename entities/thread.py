from entities.entity_util import *
from entities.links import Links
from entities.permission import Permissions
from entities.thread_prefix import ThreadPrefix


class Thread:
    thread_id: int
    forum_id: int
    thread_title: str
    thread_view_count: int
    creator_user_id: int
    creator_username: str
    thread_create_date: datetime
    thread_update_date: datetime
    user_is_ignored: bool
    thread_post_count: int
    thread_is_published: bool
    thread_is_deleted: bool
    thread_is_sticky: bool
    thread_is_followed: bool
    thread_prefixes: List[ThreadPrefix]
    thread_tags: List[Any]
    links: Links
    permissions: Permissions

    def __init__(self, thread_id: int, forum_id: int, thread_title: str, thread_view_count: int, creator_user_id: int,
                 creator_username: str, thread_create_date: datetime, thread_update_date: datetime, user_is_ignored: bool,
                 thread_post_count: int, thread_is_published: bool, thread_is_deleted: bool, thread_is_sticky: bool,
                 thread_is_followed: bool, thread_prefixes: List[ThreadPrefix], thread_tags: List[Any], links: Links,
                 permissions: Permissions) -> None:
        self.thread_id = thread_id
        self.forum_id = forum_id
        self.thread_title = thread_title
        self.thread_view_count = thread_view_count
        self.creator_user_id = creator_user_id
        self.creator_username = creator_username
        self.thread_create_date = thread_create_date
        self.thread_update_date = thread_update_date
        self.user_is_ignored = user_is_ignored
        self.thread_post_count = thread_post_count
        self.thread_is_published = thread_is_published
        self.thread_is_deleted = thread_is_deleted
        self.thread_is_sticky = thread_is_sticky
        self.thread_is_followed = thread_is_followed
        self.thread_prefixes = thread_prefixes
        self.thread_tags = thread_tags
        self.links = links
        self.permissions = permissions

    @staticmethod
    def from_dict(obj: Any) -> 'Thread':
        assert isinstance(obj, dict)
        thread_id = from_int(obj.get("thread_id"))
        forum_id = from_int(obj.get("forum_id"))
        thread_title = from_str(obj.get("thread_title"))
        thread_view_count = from_int(obj.get("thread_view_count"))
        creator_user_id = from_int(obj.get("creator_user_id"))
        creator_username = from_str(obj.get("creator_username"))
        thread_create_date = from_timestamp(obj.get("thread_create_date"))
        thread_update_date = from_timestamp(obj.get("thread_update_date"))
        user_is_ignored = from_bool(obj.get("user_is_ignored"))
        thread_post_count = from_int(obj.get("thread_post_count"))
        thread_is_published = from_bool(obj.get("thread_is_published"))
        thread_is_deleted = from_bool(obj.get("thread_is_deleted"))
        thread_is_sticky = from_bool(obj.get("thread_is_sticky"))
        thread_is_followed = from_bool(obj.get("thread_is_followed"))
        thread_prefixes = from_list(ThreadPrefix.from_dict, obj.get("thread_prefixes"))
        thread_tags = from_list(lambda x: x, obj.get("thread_tags"))
        links = Links.from_dict(obj.get("links"))
        permissions = Permissions.from_dict(obj.get("permissions"))
        return Thread(thread_id, forum_id, thread_title, thread_view_count, creator_user_id, creator_username,
                      thread_create_date, thread_update_date, user_is_ignored, thread_post_count, thread_is_published,
                      thread_is_deleted, thread_is_sticky, thread_is_followed, thread_prefixes, thread_tags, links,
                      permissions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["thread_id"] = from_int(self.thread_id)
        result["forum_id"] = from_int(self.forum_id)
        result["thread_title"] = from_str(self.thread_title)
        result["thread_view_count"] = from_int(self.thread_view_count)
        result["creator_user_id"] = from_int(self.creator_user_id)
        result["creator_username"] = from_str(self.creator_username)
        result["thread_create_date"] = date_to_timestamp(self.thread_create_date)
        result["thread_update_date"] = date_to_timestamp(self.thread_update_date)
        result["user_is_ignored"] = from_bool(self.user_is_ignored)
        result["thread_post_count"] = from_int(self.thread_post_count)
        result["thread_is_published"] = from_bool(self.thread_is_published)
        result["thread_is_deleted"] = from_bool(self.thread_is_deleted)
        result["thread_is_sticky"] = from_bool(self.thread_is_sticky)
        result["thread_is_followed"] = from_bool(self.thread_is_followed)
        result["thread_prefixes"] = from_list(lambda x: to_class(ThreadPrefix, x), self.thread_prefixes)
        result["thread_tags"] = from_list(lambda x: x, self.thread_tags)
        result["links"] = to_class(Links, self.links)
        result["permissions"] = to_class(Permissions, self.permissions)
        return result
