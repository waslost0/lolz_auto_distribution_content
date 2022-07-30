from entities.entity_util import *


class Links:
    permalink: str
    detail: str
    avatar: str
    avatar_big: str
    avatar_small: str
    followers: str
    followings: str
    ignore: str
    timeline: str
    pages: int
    page: int
    next: str

    def __init__(self, permalink: str, detail: str, avatar: str, avatar_big: str, avatar_small: str, followers: str,
                 followings: str, ignore: str, timeline: str, pages: int, page: int, nextUrl: str) -> None:
        self.permalink = permalink
        self.detail = detail
        self.avatar = avatar
        self.avatar_big = avatar_big
        self.avatar_small = avatar_small
        self.followers = followers
        self.followings = followings
        self.ignore = ignore
        self.timeline = timeline
        self.pages = pages
        self.page = page
        self.next = nextUrl

    @staticmethod
    def from_dict(obj: Any) -> 'Links':
        assert isinstance(obj, dict)
        permalink = from_str(obj.get("permalink"))
        detail = from_str(obj.get("detail"))
        avatar = from_str(obj.get("avatar"))
        avatar_big = from_str(obj.get("avatar_big"))
        avatar_small = from_str(obj.get("avatar_small"))
        followers = from_str(obj.get("followers"))
        followings = from_str(obj.get("followings"))
        ignore = from_str(obj.get("ignore"))
        pages = from_int(obj.get("pages"))
        page = from_int(obj.get("page"))
        nextUrl = from_str(obj.get("next"))
        timeline = from_str(obj.get("timeline"))
        return Links(permalink, detail, avatar, avatar_big, avatar_small, followers, followings, ignore, timeline,
                     pages, page, nextUrl)

    def to_dict(self) -> dict:
        result: dict = {}
        result["permalink"] = from_str(self.permalink)
        result["detail"] = from_str(self.detail)
        result["avatar"] = from_str(self.avatar)
        result["avatar_big"] = from_str(self.avatar_big)
        result["avatar_small"] = from_str(self.avatar_small)
        result["followers"] = from_str(self.followers)
        result["followings"] = from_str(self.followings)
        result["ignore"] = from_str(self.ignore)
        result["timeline"] = from_str(self.timeline)
        result["pages"] = from_int(self.pages)
        result["page"] = from_int(self.page)
        result["next"] = from_str(self.next)
        return result
