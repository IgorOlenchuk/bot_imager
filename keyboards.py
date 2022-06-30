from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_1 = InlineKeyboardButton('Добавить Olenchuk_Imager в свой чат', url='http://t.me/siteshot_bot?startgroup=true')
inline_btn_2 = InlineKeyboardButton('Выбор языка', callback_data='btn2')
inline_kb_full = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2)