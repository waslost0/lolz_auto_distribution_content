import json
import os
import sys
from datetime import datetime

import requests
from loguru import logger
from requests import RequestException


def load_data_from_file() -> dict:
    try:
        if not os.path.exists('data.json'):
            with open('data.json', 'w', encoding="utf-8") as f:
                data = {
                    "items_count": 1,
                    "theme_url": "https://lolz.guru/threads/ID",
                    "message": ":cutedog:",
                    "answer_as_comment": True,
                    "minimum_user_likes": 20,
                    "timeout_to_send_acc_in_minutes": 500,
                    "sleep_time": 50,
                    "lolz_api_key": "",
                    "lolz_api_url": "api.lolz.guru",
                    "telegram": {
                        "telegram_id": "",
                        "bot_token": "",
                        "info_mod": True,
                        "error_mod": True,
                    },
                    "proxy": {
                        "account_proxy": [],
                        "proxy_type": "http"
                    }
                }
                f.write(json.dumps(data, indent=4))
            logger.info('Edit data.json')
            sys.exit()

        with open('data.json', 'r', encoding='utf-8') as f:
            data = f.read()
            data = json.loads(data)

    except json.decoder.JSONDecodeError as error:
        logger.error('Невалид data.json')
        logger.error(error)
        return {}
    except KeyError as error:
        logger.error(error)
        logger.error('Cannot find: %s', error.args[0])
    else:
        return data


DATA_JSON = load_data_from_file()


def get_current_time() -> str:
    return ':'.join(datetime.now().strftime("%H:%M:%S").split(':'))


def telegram_bot_send_text(bot_message, is_silent=False):
    bot_token = DATA_JSON.get('telegram').get('bot_token')
    bot_chat_id = DATA_JSON.get('telegram').get('telegram_id')

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': bot_chat_id,
        'text': bot_message
    }

    if is_silent:
        data['disable_notification'] = 'true'

    try:
        response = requests.get(url, data=data)
        logger.info(str(response.json()))
    except RequestException as e:
        logger.error(e)
        logger.error('Fail to send telegram message')
