# lolz_auto_distribution_content

Автораздача lolz.guru строк с файла


[comment]: <> (<img src="https://i.imgur.com/9i8EX9V.png" alt="image" height="700"></img>)

## Requirements

- Python 3.8
- Бот в телеграм

## Настройка

### Установка

```shell
git clone https://github.com/waslost0/lolz_live_chat_telegram_bot
cd lolz_live_chat_telegram_bot
pip instal -r requirements.txt
```

Или скачиваем репозиторий, в папке запускаем install_libs.bat

---

### API Token lolz.guru

1) [API для разработчика](https://lolz.guru/account/api)
2) `Add New Client`
3) Заполняем данные
4) `Сохранить`
5) Копируем `API Key` и вставляем за место `CLIENT_ID` в ссылку
6) https://lolz.guru/api/index.php?oauth/authorize&response_type=token&client_id=CLIENT_ID&scope=read+post
7) Переходим по ссылке, в адресной строке отобразится токен для доступа к аккаунту `lolz_api_key`

---

### Настройка конфига

- Запустить `main.py` или `run.bat`, чтобы появился `data.json` (если нет)

### data.json

```json
{
  "items_count": 1,
  "theme_url": "",
  "message": "",
  "minimum_user_likes": 0,
  "user_timeout_to_send_trade_offer_in_minutes": 100,
  "lolz_api_key": "",
  "sleep_time": 100,
  "telegram": {
    "bot_token": "",
    "telegram_id": "",
    "info_mode": true,
    "error_mode": true
  },
  "proxy": {
    "account_proxy": "",
    "proxy_type": "https"
  }
}
```

| Параметры                      |Описание       |Обязателен к заполнению|
| -------------------------------|:----------------------------------------------------------|---|
| theme_url                      | ссылка на тему                                            |Да |
| message                        | сообщение, что будет отправлено в тему                    |Нет|
| minimum_user_likes             | количество лайков пользователя                            | - |
| timeout_to_send_acc_in_minutes | Через какое время отправить повторно отправить строку     | - |
| lolz_api_key                   | Api ключ лолза                                            |Да |
| sleep_time                     | задержка перед проверкой новых сообщений в теме           | - |
| bot_token                      | тг бот токен                                              |Да |
| telegram_id                    | id телеги, для уведомлений                                |Да |
| info_mode                      | информация об отправленных строках                        | - |
| error_mode                     | информация об ошибках                                     | - |
| items_count                    | количество строк что будет отправлено                     | - |
| account_proxy                  | прокси для лолза вида user:pass@ip:port                   | - |

---

### Телегам бот

1) Пишем в тг боту [@BotFather](https://t.me/botfather)
2) **/newbot**
3) Вводим любое имя бота
4) Вводим username для бота, в конце должно быть **bot**
5) Копируем токен бота, вставляем в data.json в раздел "telegram" ```"bot_token": "ТУТТОКЕН"```
6) Переходим в вашего бота, запускаем его

---

## Запуск

Запустить можно с помощью файла **run.bat** или с консоли `py main.py`






