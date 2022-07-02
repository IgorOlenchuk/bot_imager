import os
import time
import whois
import logging
import validators
import keyboards as kb
import messages as mes
import psycopg2

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from psycopg2.extras import LoggingConnection
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


load_dotenv()
logging.basicConfig(
        level=logging.DEBUG,
        filename='program.log',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)
# Тут установлены настройки логгера
logger = logging.getLogger(__name__)
# Устанавливаем уровень, с которого логи будут сохраняться в файл
logger.setLevel(logging.INFO)
# Указываем обработчик логов
handler = RotatingFileHandler(
    'my_logger.log',
    maxBytes=50000000,
    backupCount=5)
logger.addHandler(handler)
logger.debug('123')
logger.info('Сообщение отправлено')
logger.warning('Большая нагрузка!')
logger.error('Бот не смог отправить сообщение')
logger.critical('Всё упало! Зовите админа!1!111')
# Делаем язык по умолчанию "Русский"
# можно было и от пользователя получить locate, но пока так...
language = 'RU'
# Создаем форматер
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
# для логирования в БД, необходимо заранее создать БД на сервере
# + создать таблицу (например - сотрудники "employee")
# db_settings = {
#     "user": os.getenv('POSTGRES_USER'),
#     "password": os.getenv('POSTGRES_PASSWORD'),
#     "host": os.getenv('DB_HOST'),
#     "database" : os.getenv('DB_NAME'),
#     "port" : os.getenv('DB_PORT'),
# }
# conn = psycopg2.connect(
#    connection_factory = LoggingConnection, **db_settings)
# LoggingConnection.initialize(conn, logger)
# cur = conn.cursor()
# cur.execute("CREATE TABLE bot_log()")
# cur.execute("SELECT * FROM bot_log" )
# Указываем путь на токены бота "файл .env"
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
# Указываем путь к firefox на сервере
binary = FirefoxBinary('/bin/firefox')
options = FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    text = mes.start[language]
    await msg.answer(text=text, reply_markup=kb.inline_kb_full[language])


@dp.callback_query_handler(lambda c: c.data == 'btn_lang')
async def process_callback_btn_lang(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        mes.varible,
        reply_markup=kb.inline_lang)


@dp.callback_query_handler(lambda c: c.data == 'btn_en')
async def process_callback_btn_btn_en(callback_query: types.CallbackQuery):
    # Меняем глобальную переменную language на Английский
    global language
    language = 'EN'
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        mes.start[language],
        reply_markup=kb.inline_kb_full[language])


@dp.callback_query_handler(lambda c: c.data == 'btn_ru')
async def process_callback_btn_btn_tu(callback_query: types.CallbackQuery):
    # Меняем глобальную переменную language на Русский
    global language
    language = 'RU'
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        mes.start[language],
        reply_markup=kb.inline_kb_full[language])


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(mes.help[language])


# Ссылка на сайт имеет шаблон простого текста,
# но внутри мы ловим исключения, если сслыка введена не корректно
@dp.message_handler()
async def get_screenshot(msg: types.Message):
    url = ""
    try:
        uid = msg.chat.id
        url = msg.text
    except IndexError:
        await msg.answer(mes.no_imput[language])
        return

    if not validators.url(f'https://{url}'):
        await msg.answer(mes.err_imput[language])
    else:
        msg = await msg.answer(mes.wait[language])
        photo_path = f'screenshots/{msg.date}_{uid}_{url}.png'
        browser = webdriver.Firefox(options=options)
        browser.set_window_size(1280, 1280)
# Начинаем отчет времени выполнения запроса
        tic = time.perf_counter()
        browser.get(f'https://{url}')
        browser.save_screenshot(photo_path)
        browser.quit()
        whois_info = whois.whois(url)

# Окончаение времени выполнения запроса
        toc = time.perf_counter()

# Подгружаем кнопку под скриншотом, со встроенной ссылкой на whois
        inline_btn_3 = InlineKeyboardButton(
            mes.detailed[language],
            url=f'https://whois.ru/?domain={url}',
            show_alert=True)
        inline_kb_3 = InlineKeyboardMarkup(row_width=1).add(inline_btn_3)
        await bot.send_photo(msg.chat.id,
                             photo=open(photo_path, 'rb'),
                             caption=f'{whois_info.domain_name}, '
                                     f'{mes.domen_name[language]} '
                                     f'{url}, {mes.processing_time[language]}: '
                                     f'{toc - tic:0.4f} '
                                     f'{mes.seconds[language]}',
                             reply_markup=inline_kb_3)

# После выполнения запроса, удаляем текст "Подождите, информация загружается"
        await msg.delete()


if __name__ == '__main__':
    executor.start_polling(dp, timeout=40.0)
