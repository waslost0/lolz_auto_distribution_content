# -*- coding: utf-8 -*-
import codecs
import datetime
import json
import logging
import os
import random
import sys
import time
from datetime import datetime
from typing import Optional, List

import requests
from loguru import logger
from requests import RequestException

from api.api_response_parser import ApiResponseParser
from api.request import RequestApi
from entities.links import Links
from entities.post import Post
from entities.user import User
from entities.user_data import UserData
from utils import telegram_bot_send_text, DATA_JSON

config = {
    "handlers": [
        {"sink": sys.stderr, "level": logging.DEBUG, "backtrace": True},
        {"sink": "logs.log", "level": "DEBUG", "rotation": "5 MB", "encoding": "utf8", "backtrace": True,
         "retention": "1 day"},
    ],
}

logger.configure(**config)


class LolzWorker(RequestApi, ApiResponseParser):
    """
    Lolz worker. Auto participate in contests.
    """

    def __init__(self, user_data):
        """
        Constructor.
        """
        self.user_data: UserData = UserData.from_dict(user_data)
        super().__init__(
            lolz_api_token=self.user_data.lolz_api_key,
            api_url=self.user_data.lolz_api_url
        )
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

        self.user: Optional[User] = None
        self.last_page: Optional[int] = None
        self.is_proxy: bool = False
        self.is_telegram_info_mode: bool = False
        self.is_telegram_debug_mode: bool = False

        if self.user_data.telegram.telegram_id:
            self.is_telegram_info_mode = self.user_data.telegram.info_mod
            self.is_telegram_debug_mode = self.user_data.telegram.error_mod

        if self.user_data.proxy.account_proxy:
            self.is_proxy = True
            if not self.proxy_check():
                logger.info('Proxy set error')
                if self.is_telegram_debug_mode:
                    telegram_bot_send_text('Proxy set error')
                sys.exit('Proxy error')

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
        self.save_to_file(file_name='data.json', data=self.user_data.to_dict(), is_json=True)
        self.save_to_file(file_name='replied_users.json', data=self.replied_users, is_json=True)
        self.save_to_file(file_name='accounts.txt', data=self.accounts_list, is_json=False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_data_to_files()
        if self.is_telegram_debug_mode:
            telegram_bot_send_text(f'{str(exc_val)}')
        logger.error('exit exception text: %s' % exc_val)

    def random_proxy(self):
        proxy: dict = {
            'https': f"{self.user_data.proxy.proxy_type}://{random.choice(self.user_data.proxy.account_proxy)}",
        }
        self.session.proxies.update(proxy)

    def proxy_check(self) -> bool:
        self.random_proxy()

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
                    logger.info(self.session.proxies)
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
                telegram_bot_send_text(f'Proxy set error!\n{error}')
            sys.exit('Proxy set error!')

    @logger.catch()
    def reply_user_message(self, user: str, users_to_reply: dict):
        data_now = round(datetime.timestamp(datetime.now()))

        string_message = ''
        accounts_send = []
        for i in range(self.user_data.items_count):
            account = self.accounts_list.pop()
            accounts_send.append(account)
            string_message += account + '\n'
        post_body_message = f'[USERS={users_to_reply[user]["poster_username"]}]@{users_to_reply[user]["poster_username"]}, {self.user_data.message}\n{string_message}[/USERS]'
        data = {
            'thread_id': self.user_data.thread_id,
            'quote_post_id': users_to_reply[user]['post_id'],
            'post_body': post_body_message
        }
        try:
            if self.user_data.answer_as_comment:
                del data['post_body']
                del data['quote_post_id']
                del data['thread_id']
                data['comment_body'] = "Lorem Ipsum is simply dummy text of the"
                response = self.send_post_request(
                    path=f'posts/{users_to_reply[user]["post_id"]}/comments',
                    params=data
                )
            else:
                response = self.send_post_request(path=f'posts', params=data)

            if not response.is_error() and self.is_telegram_info_mode:
                telegram_bot_send_text(f'Отправил: {users_to_reply[user]["poster_username"]}')
            logger.info(response.dataJson)
        except (RequestException, json.decoder.JSONDecodeError) as e:
            self.random_proxy()
            logger.error(e)
            [self.accounts_list.append(item) for item in accounts_send]
        else:
            if response.is_error():
                return
            self.replied_users[user]['posts'][users_to_reply[user]['post_id']] = data_now
            self.save_to_file(file_name='replied_users.json', data=self.replied_users, is_json=True)
            self.save_to_file(file_name='accounts.txt', data=self.accounts_list, is_json=False)

        logger.info(f'Отправил: {users_to_reply[user]["poster_username"]}')

    @logger.catch()
    def reply(self):
        """

        """
        users_to_reply = []
        self.user = self.get_user_me()
        self.last_page = self.get_last_page()

        time_sleep = self.user_data.sleep_time
        while True:
            if not self.user:
                self.user = self.get_user_me()
            if not self.last_page:
                self.last_page = self.get_last_page()
            if len(self.accounts_list) <= self.user_data.items_count:
                logger.error('Accounts are EMPTY!')
                telegram_bot_send_text('Accounts are EMPTY!')
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

                            if minutes > self.user_data.user_timeout_to_send_acc_in_minutes:
                                logger.info(users_to_reply[user])
                                self.reply_user_message(user, users_to_reply)
                            else:
                                data_now = round(datetime.timestamp(datetime.now()))
                                self.replied_users[user]['posts'][users_to_reply[user].get('post_id')] = data_now
                    elif user not in self.replied_users:
                        logger.info(users_to_reply[user])
                        data_now = round(datetime.timestamp(datetime.now()))
                        self.replied_users[user] = {
                            'posts': {
                                users_to_reply[user].get('post_id'): data_now
                            },
                            'poster_username': users_to_reply[user].get('poster_username'),
                        }

                        self.reply_user_message(user, users_to_reply)
                    elif len(self.accounts_list) <= self.user_data.items_count:
                        logger.error('Accounts are EMPTY!')
                        telegram_bot_send_text('Accounts are EMPTY!')
                        time.sleep(100)
                        break

                    time.sleep(15)
            users_to_reply = {}
            logger.info(f'Sleep:{time_sleep}')
            time.sleep(time_sleep)

    def get_last_page(self) -> int:
        try:
            data = {
                "thread_id": self.user_data.thread_id,
            }
            response = self.send_get_request(path="posts", params=data)
            links: Links = ApiResponseParser.parse_object_from_response(
                response.dataJson,
                Links.from_dict,
                key="links").data

            return links.pages if links is not None and links.pages is not None else 1
        except Exception as error:
            self.random_proxy()
            logger.error(error)
            return 1

    @logger.catch()
    def get_users_to_reply(self) -> dict:
        self.random_proxy()
        users_to_reply = {}
        first_page = 1
        if int(self.last_page) > 1:
            first_page = int(self.last_page) - 1

        for i in range(first_page, int(self.last_page) + 1):
            try:
                data = {
                    "thread_id": self.user_data.thread_id,
                    "page": i
                }
                response = self.send_get_request(path="posts", params=data)

                links: Links = ApiResponseParser.parse_object_from_response(
                    response.dataJson,
                    Links.from_dict,
                    key="links").data
                posts: List[Post] = ApiResponseParser.parse_list_from_response(
                    response.dataJson,
                    from_json=Post.from_dict,
                    key='posts').data

            except Exception as error:
                self.random_proxy()
                logger.error(error)
                return users_to_reply

            if links and links.pages is not None:
                self.last_page = links.pages
                logger.info(self.last_page)

            for post in posts:
                if post.poster_user_id in self.replied_users:
                    if post.post_id in self.replied_users[post.poster_user_id].get('posts'):
                        continue

                if not post.post_is_first_post and post.poster_user_id != self.user.user_id:
                # if not post.post_is_first_post:
                    if self.user_data.minimum_user_likes > 0:
                        user_likes = self.get_user_likes(post.poster_user_id)

                        if user_likes and user_likes >= self.user_data.minimum_user_likes:
                            users_to_reply[post.poster_user_id] = {
                                'post_id': post.post_id,
                                'poster_username': post.poster_username,
                            }
                        elif user_likes:
                            data_now = round(datetime.timestamp(datetime.now()))
                            self.replied_users[post.poster_user_id] = {
                                'posts': {
                                    post.post_id: data_now
                                },
                                "poster_username": post.poster_username,
                            }
                            self.save_to_file(file_name='replied_users.json', data=self.replied_users, is_json=True)

                    else:
                        users_to_reply[post.poster_user_id] = {
                            'post_id': post.post_id,
                            'poster_username': post.poster_username,
                        }
        return users_to_reply

    @logger.catch()
    def get_user_me(self) -> Optional[User]:
        try:
            response = self.send_get_request(path='users/me')
            user = ApiResponseParser.parse_object_from_response(
                response.dataJson,
                from_json=User.from_dict,
                key='user').data
            return user
        except Exception as error:
            self.random_proxy()
            logger.error(error)
            sys.exit()

    def get_user_likes(self, user_id) -> Optional[int]:
        try:
            response = self.send_get_request(path=f'users/{user_id}')
            user: Optional[User] = ApiResponseParser.parse_object_from_response(
                response.dataJson,
                from_json=User.from_dict,
                key='user').data

            if user:
                like_count = user.user_like_count
                logger.debug(f'Get user likes count user_id:{user_id}| like_count:{like_count}')
                return like_count
        except (RequestException, json.decoder.JSONDecodeError) as error:
            self.random_proxy()
            logger.error(error)
        else:
            return None


if __name__ == '__main__':
    with LolzWorker(DATA_JSON) as lolz:
        lolz.reply()
