# Bot-imager
## Тестовое задание
[![bot_imager](https://github.com/igorolenchuk/bot_imager/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/IgorOlenchuk/bot_imager/actions/workflows/main.yml)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

# Index
  - [Описание](#описание)
  - [Полный текст задания](#полный-текст-задания)
  - [Локальное использование](#локальное-использование)
  - [Deploy](#deploy)

<br><br>
**[⬆ Back to Index](#index)**
## Описание
**bot_imager** — Telegram Bot. Бот для создания веб-скриншотов.<br>
Чтобы получить скриншот - отправьте URL адрес сайта. Например, https://wikipedia.org.<br>
• С помощью бота вы можете проверять подозрительные ссылки. (Айпилоггеры, фишинговые веб-сайты, скримеры и т.п)<br>
• Вы также можете добавить меня в свои чаты, и я смогу проверять ссылки, которые отправляют пользователи.<br>
bot_imager. использует geckodriver.<br>
Работает с протоколами https.<br>
рабочая версия бота залита на VPS с Ubuntu: https://t.me/Olenchuk_bot <br>
docker image: ashmanx/bot_imager
<br><br>
**[⬆ Back to Index](#index)**
### Полный текст задания
Напиши клон телеграм-бота @siteshot_bot, который присылает скриншот веб-страницы в ответ на
присланную боту ссылку.

*Требования:*<br>
- Python 3.x <br>

```Выполнение каждого технического требования, кроме первого, оценивается в 1 балл. Техническое
требование #1 не оценивается. Выполнение функциональных требований, кроме помеченных как “бонус”,
оценивается так же в 1 балл.
Всего для прохождения на следующий этап нужно набрать не меньше 15 баллов.
Бонус-баллы также могут быть назначены за: документацию в коде, юнит-тесты, архитектуру, позволяющую масштабировать обработку запросов от пользователей в режиме он-лайн, реализацию админинстративного интерфейса для бота, другие полезные расширения возможностей бота
Срок выполнения 7 дней.
```
<br><br>
**[⬆ Back to Index](#index)**
## Локальное использование

1) Создаем `.env` и заполняем переменные окружения, например:

```shell
vim .env
```
```text
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
TELEGRAM_TOKEN='<'токен от бота'>'
```
2) Устанавливаем [Docker](https://docs.docker.com/engine/install/)
3) Собираем `docker` в detach mode (background):
```shell
docker pull ashmanx/bot_imager
```
# 6) Наполняем `Postgres` данными:
```shell
docker-compose exec web python3 manage.py loaddata fixture.json
```
# 7) Останавливаем и удаляем контейнеры, сети, тома и образы:
```shell
docker-compose down -v --remove-orphans
```
<br><br>
**[⬆ Back to Index](#index)**
## Deploy
1) Выдать права на запуск данных скриптов: 
```shell
chmod +x ./blog/entrypoint.sh && chmod +x ./blog/entrypoint.prod.sh
```
2) Создать образ и запустить контейнер в фоне:
```shell
docker-compose -f docker-compose.yml up -d --build
```
5) Заполнить таблицы подготовленными данными. `3-4` можно пропустить - сразу запустить этот пункт
```shell
docker-compose -f docker-compose.yml exec web python bot.py fill_db
```

### Автор
Игорь Оленчук

Технические требования
1 Бот должен быть написан на языке Python - сделано
2 Все настройки бот должен брать из переменных окружения или .env файла  - сделано
3 Бот и необходимые ему сервисы должны разворачиваться в контейнерах с помощью Docker Compose - сделано
4 Зависимости бота указаны в requirements.txt с версиями или с помощью инструментов вроде Poetry - сделано через pip freeze > requirements.txt 
5 Для бота есть инструкция по его развёртыванию в README.md проекта - сделано
6 Бот логгирует свою работу с использованием библиотеки logging или loguru - сделано logging

7 Перезапуск контейнеров не должен приводить к потере данных
8 (бонус +1 балл) Процесс получения скриншота не должен блокировать работу бота (бот должен
продолжать отвечать на сообщения от других пользователей) - нет

Функциональные требования
2 По команде /start бот встречает пользователя сообщением-приветствием, которое рассказывает о
функционале бота. - сделано
3 При получении сообщения с ссылкой, бот присылает сообщение-заглушку, о том что запрос принят, и
запускает процесс получения скриншота в фоне. - сделано немного по другому, суть та же.
4 Когда скриншот получен, бот редактирует сообщение-заглушку:
a. Прикрепляет скриншот к сообщению - сделано
b. Заменяет текст сообщения на заголовок сайта, URL и время обработки страницы - сделано
c. (бонус 1 балл) добавляет к сообщению кнопку “Подробнее”, которая показывает WHOIS сайта - сделано
5 Скриншоты бот так же сохраняет в файловую систему. В имени файла обязательно должны быть: дата
запроса, user_id пользователя, домен из url запроса. - сделано
7 (бонус 1 балл) Бот позволяет выбрать язык работы - русский или английский. После переключения
языка все последующие сообщения от бота выводятся на выбранном языке. - сделано

1 Бот работает и в личных сообщениях и при добавлении в чат. - не сделал
6 (бонус 5 баллов) Бот сохраняет статистику о своей работе в базу данных - PostgreSQL или ClickHouse
Бонусные баллы за статистику начисляются по секретным правилам - попробывал сделать на PostgreSQL.
(в PostgeSQL создаем базу данных, использовал psql -> CREATE DATABASE botimager_db; Далее создаем логин и пароль и наделяем правам, а уже потом подсоединяемся к базе данных (всё также через psql) -> \с botimager login host port)