import json
import time

import requests
from fake_useragent import UserAgent
from loguru import logger
from entities.base_api_response import BaseApiResponse


class RequestApi:

    def __init__(self, lolz_api_token: str, api_url: str = 'api_url'):
        assert lolz_api_token is None or lolz_api_token != '', 'Токен не может быть пустым'

        self.ua = UserAgent(verify_ssl=False)
        self.session = requests.Session()
        self.session.headers['Authorization'] = f'Bearer {lolz_api_token}'
        self.api_url = api_url

    @logger.catch()
    def send_get_request(self, path: str, params: dict = None) -> BaseApiResponse:
        time.sleep(3.5)
        try:
            url = f"https://{self.api_url}/{path}"
            response = self.session.get(url, params=params)
            logger.info(response.text)
            return BaseApiResponse.from_dict(response.json())
        except requests.exceptions.RequestException as error:
            logger.error(error)
            return BaseApiResponse(errors=[str(error)])

    @logger.catch()
    def send_post_request(self, path: str, params: dict = None) -> BaseApiResponse:
        time.sleep(3.5)
        try:
            url = f"https://{self.api_url}/{path}"
            response = self.session.post(url, data=params)
            return BaseApiResponse.from_dict(response.json())
        except requests.exceptions.RequestException as error:
            logger.error(error)
            return BaseApiResponse(errors=[str(error)])
