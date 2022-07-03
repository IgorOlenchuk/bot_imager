# Olenchuk_BOT

Index
Описание
Полный текст задания
Локальное использование
Deploy


⬆ Back to Index

Описание
Привет! Меня зовут Olencuhk_Imager.\n' \
'Я - Бот для создания веб-скриншотов.\n' \
'Чтобы получить скриншот - отправьте URL адрес сайта. Например, https://wikipedia.org.\n' \
'• С помощью бота вы можете проверять подозрительные ссылки. (Айпилоггеры, фишинговые веб-сайты, скримеры и т.п)\n' \
'• Вы также можете добавить меня в свои чаты, и я смогу проверять ссылки, которые отправляют пользователи.\n' \
'Olencuhk_Imager. использует geckodriver.\n' \
'Работает с протоколами https.\n' \
'И находится в постоянной разработке.\n'),


⬆ Back to Index

Полный текст задания
Напиши клон телеграм-бота @siteshot_bot, который присылает скриншот веб-страницы в ответ на
присланную боту ссылку.

Требования:

Python 3.x
Выполнение каждого технического требования, кроме первого, оценивается в 1 балл. Техническое
требование #1 не оценивается. Выполнение функциональных требований, кроме помеченных как “бонус”,
оценивается так же в 1 балл.
Всего для прохождения на следующий этап нужно набрать не меньше 15 баллов.
Бонус-баллы также могут быть назначены за:
1 документацию в коде
2 юнит-тесты
3 архитектуру, позволяющую масштабировать обработку запросов от пользователей в режиме он-лайн
4 реализацию админинстративного интерфейса для бота
5 другие полезные расширения возможностей бота
Срок выполнения 7 дней.
Ссылку на гитхаб отправить на info@nekidaem.ru.


⬆ Back to Index

Локальное использование
Создаем .env и заполняем переменные окружения, например:
vim .env
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
Устанавливаем Docker
Собираем docker-compose в detach mode (background):
docker-compose up --build -d --force-recreate
Наполняем Postgres данными:
docker-compose exec web python3 manage.py loaddata fixture.json
Останавливаем и удаляем контейнеры, сети, тома и образы:
docker-compose down -v --remove-orphans


⬆ Back to Index

Deploy
Выдать права на запуск данных скриптов:
chmod +x ./blog/entrypoint.sh && chmod +x ./blog/entrypoint.prod.sh
Создать образ и запустить контейнер в фоне:
docker-compose -f docker-compose.yml up -d --build

Автор
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