# -*- coding: utf-8 -*-
import codecs
import datetime
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from typing import Union

import requests
from fake_useragent import UserAgent
from loguru import logger
from requests import RequestException

# https://zelenka.guru/api/index.php?oauth/authorize&response_type=token&client_id=CLIENT_ID&scope=read+post
from utils import telegram_bot_send_text, DATA_JSON

config = {
    "handlers": [
        {"sink": sys.stderr, "level": logging.DEBUG, "backtrace": True},
        {"sink": "logs.log", "level": "DEBUG", "rotation": "5 MB", "encoding": "utf8", "backtrace": True,
         "retention": "1 day"},
    ],
}

logger.configure(**config)


class LolzWorker:
    """
    Lolz worker. Auto participate in contests.
    """

    def __init__(self, user_data):
        """
        Constructor.
        """
        self.ua = UserAgent(verify_ssl=False)
        self.session = requests.Session()
        self.domain_name = 'zelenka.guru'
        self.user_data = user_data
        self.session.headers['Authorization'] = 'Bearer ' + self.user_data.get("lolz_api_key")
        self.theme_url = user_data['theme_url']
        if not os.path.exists('replied_users.json'):
            with open('replied_users.json', 'w', encoding="utf-8") as f:
                data = {}
                f.write(json.dumps(data, indent=4))

        if not os.path.exists('accounts.txt'):
            with open('accounts.txt', 'w', encoding="utf-8") as f:
                logger.error('Empty accounts.txt')
                f.write('\n')
                sys.exit()
        self.accounts_list = []

        with open('replied_users.json', 'r', encoding="utf-8") as f:
            self.replied_users = json.load(f)

        with codecs.open('accounts.txt', 'r', encoding='utf-8') as f:
            self.accounts_list = f.read().splitlines()

        self.thread_id = None
        self.username = None
        self.user_id = None
        self.last_page = None
        self.items_count = self.user_data.get('items_count')
        self.is_proxy = False
        self.is_telegram_info_mode = False
        self.is_telegram_debug_mode = False

        if self.user_data['telegram']['telegram_id'] != '':
            self.is_telegram_info_mode = self.user_data['telegram']['info_mod']
            self.is_telegram_debug_mode = self.user_data['telegram']['error_mod']

        if self.user_data['proxy']['account_proxy'] != '':
            self.is_proxy = True
            logger.info(self.user_data["proxy"])
            self.set_proxy()
            if not self.proxy_check():
                logger.info('Proxy set error')
                if self.is_telegram_debug_mode:
                    telegram_bot_send_text('Proxy set error', is_silent=False)
                sys.exit('Proxy error')
        self.session.post(f'https://{self.domain_name}/api/index.php?me')

    def __enter__(self):
        return self

    def save_to_file(self, file_name, data, is_json=True):
        with open(file_name, 'w', encoding="utf-8") as f:
            if is_json:
                f.write(json.dumps(data, indent=4))
            else:
                for item in self.accounts_list:
                    f.write(f'{item}\n')

    def save_data_to_files(self):
        self.save_to_file(file_name='data.json', data=self.user_data, is_json=True)
        self.save_to_file(file_name='replied_users.json', data=self.replied_users, is_json=True)
        self.save_to_file(file_name='accounts.txt', data=self.accounts_list, is_json=False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_data_to_files()
        if self.is_telegram_debug_mode:
            telegram_bot_send_text(f'{str(exc_val)}', is_silent=False)
        logger.error('exit exception text: %s' % exc_val)

    def set_proxy(self):
        proxy_type = self.user_data['proxy']['proxy_type']
        if 'http' in proxy_type:
            proxy_type = 'http'
        proxy = {
            'http': f"{proxy_type}://{self.user_data['proxy']['account_proxy']}",
            'https': f"{proxy_type}://{self.user_data['proxy']['account_proxy']}",
        }
        self.session.proxies.update(proxy)

    def proxy_check(self):
        api_urls = [
            'https://api.ipify.org?format=json',
            'https://ip.seeip.org/jsonip?',
            'https://ipwhois.app/json/',
            'https://l2.io/ip.json',
            'https://api.myip.co',
        ]

        try:
            for link in api_urls:
                try:
                    response_no_proxy = requests.get(link, timeout=5).json()
                    response_with_proxy = self.session.get(link, timeout=5).json()

                    logger.info(f'Your ip: {response_no_proxy}')
                    logger.info(f'Ip with proxy: {response_with_proxy}')

                    if response_with_proxy['ip'] == response_no_proxy['ip']:
                        return False
                    else:
                        return True
                except Exception as e:
                    logger.error(e)
        except Exception as error:
            logger.error(error)
            logger.error('Proxy set error!')
            if self.is_telegram_debug_mode:
                telegram_bot_send_text(f'Proxy set error!\n{error}', is_silent=False)
            sys.exit('Proxy set error!')

    def reply_user_message(self, user: str, users_to_reply: dict):
        now = datetime.now()
        data_now = datetime.timestamp(now)

        string_message = ''
        accounts_send = []
        for i in range(self.items_count):
            account = self.accounts_list.pop()
            accounts_send.append(account)
            string_message += account + '\n'

        if self.is_telegram_info_mode:
            telegram_bot_send_text(f'Отправил: {users_to_reply[user]["poster_username"]}', is_silent=False)
        data = {
            'thread_id': self.thread_id,
            'quote_post_id': users_to_reply[user]['post_id'],
            'post_body': f'[USERS={users_to_reply[user]["poster_username"]}]@{users_to_reply[user]["poster_username"]}, {self.user_data["message"]}\n{string_message}[/USERS]'
        }
        try:
            response = self.session.post(f'https://{self.domain_name}/api/index.php?posts', data=data).json()
            logger.info(response)
        except (RequestException, json.decoder.JSONDecodeError) as e:
            logger.error(e)
            [self.accounts_list.append(item) for item in accounts_send]
        else:
            self.replied_users[user]['posts'][users_to_reply[user]['post_id']] = data_now
            # update `replied_users.json`
            self.save_to_file(file_name='replied_users.json', data=self.replied_users, is_json=True)
            self.save_to_file(file_name='accounts.txt', data=self.accounts_list, is_json=False)

        logger.info(f'Отправил: {users_to_reply[user]["poster_username"]}')

    def reply(self):
        """

        """
        users_to_reply = []
        result = re.search(r'\d+', self.theme_url)
        self.thread_id = result.group(0)
        user = self.get_user_me()
        self.username = self.get_username(user)
        self.user_id = self.get_user_id(user)
        self.last_page = self.get_last_page()

        time_sleep = self.user_data['sleep_time']
        while True:
            if len(self.accounts_list) <= self.items_count:
                logger.error('Accounts are EMPTY!')
                telegram_bot_send_text('Accounts are EMPTY!', is_silent=False)
                break

            # Get users
            if not users_to_reply:
                logger.info('Get users to reply')
                users_to_reply = self.get_users_to_reply()

            if users_to_reply:
                for user in users_to_reply.keys():
                    if self.accounts_list and user in self.replied_users:
                        if users_to_reply[user].get('post_id') in self.replied_users[user]['posts']:
                            continue
                        else:
                            user_timestamp = list(self.replied_users[user]['posts'].values())[-1]
                            user_date = datetime.fromtimestamp(user_timestamp)
                            now = datetime.now()
                            diff = now - user_date
                            minutes = diff.total_seconds() / 60

                            if minutes > self.user_data['timeout_to_send_acc_in_minutes']:
                                logger.info(users_to_reply[user])
                                self.reply_user_message(user, users_to_reply)
                            else:
                                now = datetime.now()
                                data_now = datetime.timestamp(now)
                                self.replied_users[user]['posts'][users_to_reply[user].get('post_id')] = data_now
                    elif user not in self.replied_users:
                        logger.info(users_to_reply[user])
                        now = datetime.now()
                        data_now = datetime.timestamp(now)
                        self.replied_users[user] = {
                            'posts': {
                                users_to_reply[user].get('post_id'): data_now
                            },
                            "poster_username": users_to_reply[user].get('poster_username'),
                        }

                        self.reply_user_message(user, users_to_reply)
                    elif len(self.accounts_list) <= self.items_count:
                        logger.error('Accounts are EMPTY!')
                        telegram_bot_send_text('Accounts are EMPTY!', is_silent=False)
                        time.sleep(100)
                        break

                    time.sleep(15)
            users_to_reply = {}
            logger.info(f'Sleep:{time_sleep}')
            time.sleep(time_sleep)

    @logger.catch()
    def get_last_page(self) -> int:
        try:
            response = self.session.get(
                f'https://{self.domain_name}/api/index.php?posts/&thread_id={self.thread_id}').json()
            if 'links' in response:
                last_page = response['links']['pages']
            else:
                last_page = 1
            return last_page
        except Exception as error:
            logger.error(error)
            return 1

    @logger.catch()
    def get_users_to_reply(self) -> dict:
        users_to_reply = {}
        first_page = 1
        if int(self.last_page) > 1:
            first_page = int(self.last_page) - 1

        for i in range(first_page, int(self.last_page) + 1):
            try:
                response = self.session.get(
                    f'https://{self.domain_name}/api/index.php?posts/&thread_id={self.thread_id}&page={i}').json()
            except Exception as error:
                logger.error(error)
                return users_to_reply

            links = response.get('links')

            if links and links.get('pages'):
                self.last_page = links.get('pages')
                logger.info(self.last_page)

            for post in response['posts']:
                if str(post['poster_user_id']) in self.replied_users:
                    if str(post['post_id']) in self.replied_users[str(post['poster_user_id'])]['posts']:
                        continue
                if not post['post_is_first_post'] and str(post['poster_user_id']) != str(self.user_id):
                    if self.user_data['minimum_user_likes'] > 0:
                        user_likes = self.get_user_likes(post['poster_user_id'])
                        if user_likes and user_likes >= self.user_data['minimum_user_likes']:
                            users_to_reply[str(post['poster_user_id'])] = {
                                'post_id': str(post['post_id']),
                                'poster_username': post['poster_username'],
                            }
                        else:
                            now = datetime.now()
                            data_now = datetime.timestamp(now)
                            self.replied_users[str(post.get('poster_user_id'))] = {
                                'posts': {
                                    str(post.get('post_id')): data_now
                                },
                                "poster_username": post.get('poster_username'),
                            }
                            self.save_to_file(file_name='replied_users.json', data=self.replied_users, is_json=True)

                    else:
                        users_to_reply[str(post['poster_user_id'])] = {
                            'post_id': str(post['post_id']),
                            'poster_username': post['poster_username'],
                        }
        return users_to_reply

    def get_user_me(self) -> Union[dict, None]:
        try:
            response = self.session.get(f'https://{self.domain_name}/api/index.php?/users/me').json()
        except (RequestException, json.decoder.JSONDecodeError) as error:
            logger.error(error)
            return None
        else:
            return response

    @staticmethod
    def get_username(user: dict) -> Union[dict, None]:
        try:
            if 'user' in user:
                return user.get('user').get('username')
        except KeyError as error:
            logger.error(error)
            return None

    @staticmethod
    def get_user_id(user: dict) -> Union[str, None]:
        try:
            if 'user' in user:
                return user['user']['user_id']
        except KeyError as error:
            logger.error(error)
            return None

    def get_user_likes(self, user_id) -> Union[int, None]:
        time.sleep(3)
        try:
            response = self.session.get(f'https://{self.domain_name}/api/index.php?/users/{user_id}')
            response = response.json()
            if 'user' in response:
                like_count = response['user']['user_like_count']
                logger.debug(f'Get user likes count user_id:{user_id}| like_count:{like_count}')
                return like_count
        except (RequestException, json.decoder.JSONDecodeError) as error:
            logger.error(error)
        else:
            return None


if __name__ == '__main__':
    with LolzWorker(DATA_JSON) as lolz:
        lolz.reply()
