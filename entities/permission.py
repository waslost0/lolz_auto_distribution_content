from entities.entity_util import *


class Permissions:
    view: bool
    delete: bool
    follow: bool
    post: bool
    upload_attachment: bool

    def __init__(self, view: bool, delete: bool, follow: bool, post: bool, upload_attachment: bool) -> None:
        self.view = view
        self.delete = delete
        self.follow = follow
        self.post = post
        self.upload_attachment = upload_attachment

    @staticmethod
    def from_dict(obj: Any) -> 'Permissions':
        assert isinstance(obj, dict)
        view = from_bool(obj.get("view"))
        delete = from_bool(obj.get("delete"))
        follow = from_bool(obj.get("follow"))
        post = from_bool(obj.get("post"))
        upload_attachment = from_bool(obj.get("upload_attachment"))
        return Permissions(view, delete, follow, post, upload_attachment)

    def to_dict(self) -> dict:
        result: dict = {}
        result["view"] = from_bool(self.view)
        result["delete"] = from_bool(self.delete)
        result["follow"] = from_bool(self.follow)
        result["post"] = from_bool(self.post)
        result["upload_attachment"] = from_bool(self.upload_attachment)
        return result
