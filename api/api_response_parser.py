from typing import Callable

from entities.base_api_response import BaseApiResponse


class ApiResponseParser:
    defaultErrorMessage = 'Произошла неизвестная ошибка.'

    @staticmethod
    def parse_object_from_response(response: dict, from_json: Callable, key: str = None) -> BaseApiResponse:
        response_ = BaseApiResponse.from_dict(response)
        if response_.is_error():
            return BaseApiResponse(errors=response_.errorMessageList)

        jsonData: dict = {}
        if key:
            jsonData = response_.dataJson.get(key)
        else:
            jsonData = response_.dataJson

        if jsonData is None:
            return BaseApiResponse(errors=["Данные не найдены"])

        result = from_json(jsonData)
        response_.data = result
        return response_

    @staticmethod
    def parse_list_from_response(response: dict, from_json: Callable, key: str = None) -> BaseApiResponse:
        response_ = BaseApiResponse.from_dict(response)
        if response_.is_error():
            return BaseApiResponse(errors=response_.errorMessageList)

        jsonData: list = []
        if key:
            jsonData = response_.dataJson.get(key)
        else:
            jsonData = list(response_.dataJson)

        if jsonData is None:
            return BaseApiResponse(errors=["Данные не найдены"])

        #  final list = (jsonData as List).map((e) => fromJson(e)).toList();
        result = [from_json(i) for i in jsonData]

        response_.data = result
        return response_
