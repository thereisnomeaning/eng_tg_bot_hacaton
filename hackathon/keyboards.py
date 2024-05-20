import telebot.apihelper
from telebot import types


# Конструируем Inline клавиатуру.
def inline_menu_keyboard(options, rows):
    buttons = (types.InlineKeyboardButton(text=option, callback_data=callback) for option, callback in options)
    keyboard = types.InlineKeyboardMarkup(row_width=rows)
    keyboard.add(*buttons)
    return keyboard

# Создаем Reply клавиатуру
def menu_keyboard(options):
    buttons = (types.KeyboardButton(text=option) for option in options)
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


