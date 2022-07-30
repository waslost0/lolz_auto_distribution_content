import re

from entities.entity_util import *


class TelegramData:
    telegram_id: str
    bot_token: str
    info_mod: bool
    error_mod: bool

    def __init__(
            self,
            telegram_id: Optional[str],
            bot_token: Optional[str],
            info_mod: Optional[bool],
            error_mod: Optional[bool],
    ) -> None:
        self.telegram_id = telegram_id
        self.bot_token = bot_token
        self.info_mod = info_mod
        self.error_mod = error_mod

    @staticmethod
    def from_dict(obj: Any) -> 'TelegramData':
        telegram_id = from_str(obj.get("telegram_id"))
        bot_token = from_str(obj.get("bot_token"))
        info_mod = from_bool(obj.get("info_mod"))
        error_mod = from_bool(obj.get("error_mod"))

        return TelegramData(
            telegram_id=telegram_id,
            bot_token=bot_token,
            info_mod=info_mod,
            error_mod=error_mod,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["telegram_id"] = self.telegram_id
        result["bot_token"] = self.bot_token
        result["info_mod"] = self.info_mod
        return result


class ProxyData:
    account_proxy: List[str]
    proxy_type: str

    def __init__(
            self,
            account_proxy: Optional[List[str]],
            proxy_type: Optional[str],
    ) -> None:
        self.account_proxy = account_proxy
        self.proxy_type = proxy_type

    @staticmethod
    def from_dict(obj: Any) -> 'ProxyData':
        account_proxy = from_str(obj.get("account_proxy"))
        proxy_type = from_str(obj.get("proxy_type"))
        if 'https' in proxy_type:
            proxy_type = 'http'

        return ProxyData(
            account_proxy=account_proxy,
            proxy_type=proxy_type,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["account_proxy"] = self.account_proxy
        result["proxy_type"] = self.proxy_type
        return result


class UserData:
    items_count: int
    theme_url: str
    thread_id: int
    message: str
    answer_as_comment: bool
    minimum_user_likes: int
    user_timeout_to_send_acc_in_minutes: int
    sleep_time: int
    lolz_api_key: str
    lolz_api_url: str
    telegram: TelegramData
    proxy: ProxyData

    def __init__(
            self,
            items_count: Optional[int],
            theme_url: Optional[str],
            message: Optional[str],
            minimum_user_likes: Optional[int],
            user_timeout_to_send_acc_in_minutes: Optional[int],
            sleep_time: Optional[int],
            lolz_api_key: Optional[str],
            lolz_api_url: Optional[str],
            telegram: Optional[TelegramData],
            proxy: Optional[ProxyData],
            thread_id: Optional[int],
            answer_as_comment: Optional[bool],
    ) -> None:
        self.items_count = items_count
        self.theme_url = theme_url
        self.message = message
        self.minimum_user_likes = minimum_user_likes
        self.user_timeout_to_send_acc_in_minutes = user_timeout_to_send_acc_in_minutes
        self.sleep_time = sleep_time
        self.lolz_api_key = lolz_api_key
        self.lolz_api_url = lolz_api_url
        self.telegram = telegram
        self.proxy = proxy
        self.thread_id = thread_id
        self.answer_as_comment = answer_as_comment

    @staticmethod
    def from_dict(obj: Any) -> 'UserData':
        items_count = from_int(obj.get("items_count"))
        theme_url = from_str(obj.get("theme_url"))
        message = from_str(obj.get("message"))
        minimum_user_likes = from_int(obj.get("minimum_user_likes"))
        user_timeout_to_send_acc_in_minutes = from_int(obj.get("user_timeout_to_send_acc_in_minutes"))
        sleep_time = from_int(obj.get("sleep_time"))
        lolz_api_key = from_str(obj.get("lolz_api_key"))
        telegram = TelegramData.from_dict(obj.get("telegram"))
        proxy = ProxyData.from_dict(obj.get("proxy"))
        answer_as_comment = from_str(obj.get("answer_as_comment"))
        lolz_api_url = from_str(obj.get("lolz_api_url"))
        thread_id = UserData.get_tread_id(theme_url)

        return UserData(
            items_count=items_count,
            theme_url=theme_url,
            message=message,
            minimum_user_likes=minimum_user_likes,
            user_timeout_to_send_acc_in_minutes=user_timeout_to_send_acc_in_minutes,
            sleep_time=sleep_time,
            lolz_api_key=lolz_api_key,
            telegram=telegram,
            proxy=proxy,
            lolz_api_url=lolz_api_url,
            thread_id=thread_id,
            answer_as_comment=answer_as_comment,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["items_count"] = self.items_count
        result["theme_url"] = self.theme_url
        result["message"] = self.message
        result["lolz_api_url"] = self.lolz_api_url
        result["minimum_user_likes"] = self.minimum_user_likes
        result["user_timeout_to_send_acc_in_minutes"] = self.user_timeout_to_send_acc_in_minutes
        result["sleep_time"] = self.sleep_time
        result["lolz_api_key"] = self.lolz_api_key
        result["telegram"] = self.telegram.to_dict()
        result["proxy"] = self.proxy.to_dict()
        result["answer_as_comment"] = self.answer_as_comment
        return result

    @staticmethod
    def get_tread_id(theme_url: str) -> int:
        result = re.search(r'\d+', theme_url)
        return int(result.group(0))
