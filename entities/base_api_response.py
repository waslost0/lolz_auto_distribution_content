from dataclasses import dataclass

from entities.entity_util import *


@dataclass
class SystemInfo:
    visitor_id: int
    time: int

    def __init__(self, visitor_id: int, time: int) -> None:
        self.visitor_id = visitor_id
        self.time = time

    @staticmethod
    def from_dict(obj: Any) -> 'SystemInfo':
        assert isinstance(obj, dict)
        visitor_id = from_int(obj.get("visitor_id"))
        time = from_int(obj.get("time"))
        return SystemInfo(visitor_id, time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["visitor_id"] = from_int(self.visitor_id)
        result["time"] = from_int(self.time)
        return result


@dataclass
class BaseApiResponse:
    rawData: str
    dataJson: dict
    errorMessageList: List[str]
    message: str
    status: str
    data: T

    def __init__(self, raw: str = None, data: dict = None, errors: list = None, message: str = None,
                 status: str = None, obj: T = None) -> None:
        self.dataJson = data
        self.rawData = raw
        self.errorMessageList = errors
        self.message = message
        self.status = status
        self.data = obj

    def is_error(self) -> bool:
        return True if self.errorMessageList else False

    @staticmethod
    def from_dict(obj: Any) -> 'BaseApiResponse':
        try:
            errors = obj.get("errors")
            if type(errors) is list:
                errors = from_list(from_str, obj.get("errors"))
            elif type(errors) is dict:
                if errors.get('message'):
                    errors = [errors.get('message')]

            message = obj.get("message")
            status = obj.get("status")
            return BaseApiResponse(raw=str(obj), data=obj, errors=errors, message=message, status=status)
        except Exception as error:
            return BaseApiResponse(errors=[str(error)])

    def to_dict(self) -> dict:
        result: dict = {}
        result["dataJson"] = self.dataJson
        result["status"] = self.status
        result["message"] = self.message
        result["errorMessageList"] = self.errorMessageList
        return result


