from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import bot
import messages as mes
from bot import language

inline_btn_1 = InlineKeyboardButton(
    mes.add_tg['RU'],
    url='http://t.me/siteshot_bot?startgroup=true')
inline_btn_2 = InlineKeyboardButton(
    mes.lang['RU'],
    callback_data='btn_lang')
inline_btn_6 = InlineKeyboardButton(
    mes.add_tg['EN'],
    url='http://t.me/siteshot_bot?startgroup=true')
inline_btn_7 = InlineKeyboardButton(
    mes.lang['EN'],
    callback_data='btn_lang')
inline_kb_full = {
    'RU': InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2),
    'EN': InlineKeyboardMarkup(row_width=1).add(inline_btn_6, inline_btn_7)
    }

inline_btn_4 = InlineKeyboardButton(mes.en, callback_data='btn_en')
inline_btn_5 = InlineKeyboardButton(mes.ru, callback_data='btn_ru')
inline_lang = InlineKeyboardMarkup(row_width=2).add(inline_btn_4, inline_btn_5)

inline_btn_3 = InlineKeyboardButton(
    mes.detailed['RU'],
    callback_data='btn_detailed')
inline_btn_8 = InlineKeyboardButton(
    mes.detailed['EN'],
    callback_data='btn_detailed')
inline_kb_3 = {
    'RU': InlineKeyboardMarkup(row_width=1).add(inline_btn_3),
    'EN': InlineKeyboardMarkup(row_width=1).add(inline_btn_8)
    }


