import json
import logging
import os
import socket
import time
import urllib.request
from logging.handlers import RotatingFileHandler

# import psycopg2
import validators
import whois
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv
# from psycopg2.extras import LoggingConnection
from selenium import common, webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import keyboards as kb
import messages as mes

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
# Задаем глобальные переменные
url = ''
whois_info = whois.whois(url)
# Для логирования: создаем форматер
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
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
    await msg.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb.inline_kb_full[language])


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
    global url
    global whois_info
    try:
        uid = msg.chat.id
        url = msg.text
        whois_info = whois.whois(url)
    except IndexError:
        await msg.answer(mes.no_imput[language])
        return
    if not validators.url(f'https://{url}'):
        await msg.answer(mes.err_imput[language])
    else:
        msg = await msg.answer(mes.wait[language])
        if whois_info.dnssec == 'unsigned':
            await msg.delete()
            await msg.answer(mes.domen_free[language])
        photo_path = f'screenshots/{msg.date}_{uid}_{url}.png'
        browser = webdriver.Firefox(options=options)
        browser.set_window_size(1280, 1280)
# Начинаем отчет времени выполнения запроса,
# ловим исключения, если сайт не существует
        try:
            tic = time.perf_counter()
            browser.get(f'https://{url}')
            browser.save_screenshot(photo_path)
        except common.exceptions.WebDriverException:
            await msg.answer(mes.dns_err[language])
        else:
            browser.quit()
# Окончаение времени выполнения запроса
            toc = time.perf_counter()
    # Подгружаем кнопку под скриншотом
            await bot.send_photo(
                msg.chat.id,
                photo=open(photo_path, 'rb'),
                caption=f'{whois_info.domain_name}\n'
                        f'{mes.domen_name[language]} '
                        f'{url}\n'
                        f'{mes.processing_time[language]} '
                        f'{toc - tic:0.4f} '
                        f'{mes.seconds[language]}',
                reply_markup=kb.inline_kb_3[language])

# После выполнения запроса, удаляем текст "Подождите, информация загружается"
        await msg.delete()


@dp.callback_query_handler(lambda c: c.data == 'btn_detailed')
async def process_callback_btn_detailed(callback_query: types.CallbackQuery):
    ip = socket.gethostbyname(url)
    url_ip = f'http://ipinfo.io/{ip}/json'
    getinfo = urllib.request.urlopen(url_ip)
    data = json.load(getinfo)
    org = data['org']
    city = data['city']
    country = data['country']
    timezone = data['timezone']
    await bot.answer_callback_query(
        callback_query.id,
        text=f'IP: {ip}\n \n'
             f'{mes.timezone[language]}: {timezone}\n'
             f'{mes.country[language]}: {country}\n'
             f'{mes.city[language]}: {city}\n \n'
             f'{mes.org[language]}: {org}\n'
             f'{mes.org2[language]}: {whois_info.org}\n',
        show_alert=True)

@dp.callback_query_handler(lambda c: c.data == 'copy_url')
async def process_callback_btn_detailed(callback_query: types.CallbackQuery):
    await bot.copy_message(
        chat_id=callback_query.id,
        from_chat_id=callback_query.id,
        message_id=callback_query.message.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=40.0)
