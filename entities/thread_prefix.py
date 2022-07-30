from entities.entity_util import *


class ThreadPrefix:
    prefix_id: int
    prefix_title: str

    def __init__(self, prefix_id: int, prefix_title: str) -> None:
        self.prefix_id = prefix_id
        self.prefix_title = prefix_title

    @staticmethod
    def from_dict(obj: Any) -> 'ThreadPrefix':
        assert isinstance(obj, dict)
        prefix_id = from_int(obj.get("prefix_id"))
        prefix_title = from_str(obj.get("prefix_title"))
        return ThreadPrefix(prefix_id, prefix_title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["prefix_id"] = from_int(self.prefix_id)
        result["prefix_title"] = from_str(self.prefix_title)
        return result
