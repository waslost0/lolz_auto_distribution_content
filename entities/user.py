from entities.entity_util import *
from entities.links import Links


class User:
    user_id: int
    username: str
    user_message_count: int
    user_register_date: int
    user_like_count: int
    user_email: str
    user_unread_notification_count: int
    user_dob_day: int
    user_dob_month: int
    user_dob_year: int
    user_title: str
    user_is_valid: bool
    user_is_verified: bool
    user_is_followed: bool
    user_last_seen_date: int
    links: Links
    user_is_ignored: bool
    user_is_visitor: bool
    user_timezone_offset: int
    user_has_password: bool

    def __init__(self, user_id: int, username: str, user_message_count: int, user_register_date: int,
                 user_like_count: int, user_email: str, user_unread_notification_count: int, user_dob_day: int,
                 user_dob_month: int, user_dob_year: int, user_title: str, user_is_valid: bool, user_is_verified: bool,
                 user_is_followed: bool, user_last_seen_date: int, links: Links,
                 user_is_ignored: bool, user_is_visitor: bool, user_timezone_offset: int, user_has_password: bool) -> None:
        self.user_id = user_id
        self.username = username
        self.user_message_count = user_message_count
        self.user_register_date = user_register_date
        self.user_like_count = user_like_count
        self.user_email = user_email
        self.user_unread_notification_count = user_unread_notification_count
        self.user_dob_day = user_dob_day
        self.user_dob_month = user_dob_month
        self.user_dob_year = user_dob_year
        self.user_title = user_title
        self.user_is_valid = user_is_valid
        self.user_is_verified = user_is_verified
        self.user_is_followed = user_is_followed
        self.user_last_seen_date = user_last_seen_date
        self.links = links
        self.user_is_ignored = user_is_ignored
        self.user_is_visitor = user_is_visitor
        self.user_timezone_offset = user_timezone_offset
        self.user_has_password = user_has_password

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        user_id = from_int(obj.get("user_id"))
        username = from_str(obj.get("username"))
        user_message_count = from_int(obj.get("user_message_count"))
        user_register_date = from_int(obj.get("user_register_date"))
        user_like_count = from_int(obj.get("user_like_count"))
        user_email = from_str(obj.get("user_email"))
        user_unread_notification_count = from_int(obj.get("user_unread_notification_count"))
        user_dob_day = from_int(obj.get("user_dob_day"))
        user_dob_month = from_int(obj.get("user_dob_month"))
        user_dob_year = from_int(obj.get("user_dob_year"))
        user_title = from_str(obj.get("user_title"))
        user_is_valid = from_bool(obj.get("user_is_valid"))
        user_is_verified = from_bool(obj.get("user_is_verified"))
        user_is_followed = from_bool(obj.get("user_is_followed"))
        user_last_seen_date = from_int(obj.get("user_last_seen_date"))
        links = Links.from_dict(obj.get("links"))
        user_is_ignored = from_bool(obj.get("user_is_ignored"))
        user_is_visitor = from_bool(obj.get("user_is_visitor"))
        user_timezone_offset = from_int(obj.get("user_timezone_offset"))
        user_has_password = from_bool(obj.get("user_has_password"))
        return User(user_id, username, user_message_count, user_register_date, user_like_count, user_email,
                    user_unread_notification_count, user_dob_day, user_dob_month, user_dob_year, user_title,
                    user_is_valid, user_is_verified, user_is_followed, user_last_seen_date, links,
                    user_is_ignored, user_is_visitor, user_timezone_offset, user_has_password)

    def to_dict(self) -> dict:
        result: dict = {}
        result["user_id"] = from_int(self.user_id)
        result["username"] = from_str(self.username)
        result["user_message_count"] = from_int(self.user_message_count)
        result["user_register_date"] = from_int(self.user_register_date)
        result["user_like_count"] = from_int(self.user_like_count)
        result["user_email"] = from_str(self.user_email)
        result["user_unread_notification_count"] = from_int(self.user_unread_notification_count)
        result["user_dob_day"] = from_int(self.user_dob_day)
        result["user_dob_month"] = from_int(self.user_dob_month)
        result["user_dob_year"] = from_int(self.user_dob_year)
        result["user_title"] = from_str(self.user_title)
        result["user_is_valid"] = from_bool(self.user_is_valid)
        result["user_is_verified"] = from_bool(self.user_is_verified)
        result["user_is_followed"] = from_bool(self.user_is_followed)
        result["user_last_seen_date"] = from_int(self.user_last_seen_date)
        result["links"] = to_class(Links, self.links)
        result["user_is_ignored"] = from_bool(self.user_is_ignored)
        result["user_is_visitor"] = from_bool(self.user_is_visitor)
        result["user_timezone_offset"] = from_int(self.user_timezone_offset)
        result["user_has_password"] = from_bool(self.user_has_password)
        return result
