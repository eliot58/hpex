from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from .common import cb_main


def phone_tied_kb():
    rp = ReplyKeyboardMarkup(resize_keyboard=True)
    rp.add(KeyboardButton("Привязан"), KeyboardButton("Не привязан"))
    return rp

def is_correct_rb():
    rp = ReplyKeyboardMarkup(resize_keyboard=True)
    rp.add(KeyboardButton("Всё верно"), KeyboardButton("Нет исправить"))
    return rp

def is_correct_ik():
    ik = InlineKeyboardMarkup()
    ik.add(InlineKeyboardButton("Всё верно", callback_data=cb_main.new(action="is_correct")), InlineKeyboardButton("Нет исправить", callback_data=cb_main.new(action="is_not_correct")))
           
    return ik


def qr_code_kb():
    rp = ReplyKeyboardMarkup(resize_keyboard=True)
    rp.add(KeyboardButton("Его нет"))
    return rp


def main_keyboard():
    ik = InlineKeyboardMarkup()
    ik.add(InlineKeyboardButton("Купить ЮАНЬ", url="https://www.google.com/"), 
           InlineKeyboardButton("Контроль таблица", callback_data=cb_main.new(action="control_table")))
    ik.add(InlineKeyboardButton("Выкуп", callback_data=cb_main.new(action="ransom")),
           InlineKeyboardButton("Заполнить адрес", callback_data=cb_main.new(action="fill_address")))
    ik.add(InlineKeyboardButton("Зарегистрировать клиента", callback_data=cb_main.new(action="register")))
           
           
    return ik

def back_to_main_kb():
    ik = InlineKeyboardMarkup()
    ik.add(InlineKeyboardButton("Главное меню", callback_data=cb_main.new(action="main")))
           
    return ik

def fill_address_kb():
    ik = InlineKeyboardMarkup()
    ik.add(InlineKeyboardButton("Инструкция 1688", callback_data=cb_main.new(action="1688")))
    ik.add(InlineKeyboardButton("Инструкция Pinduoduo", callback_data=cb_main.new(action="pinduo")))
    ik.add(InlineKeyboardButton("Инструкция Poizon", callback_data=cb_main.new(action="poizon")))
    ik.add(InlineKeyboardButton("Инструкция Taobao", callback_data=cb_main.new(action="taobao")))
    ik.add(InlineKeyboardButton("Главное меню", callback_data=cb_main.new(action="main")))
           
    return ik

def table_keyboard():
    ik = InlineKeyboardMarkup()
    ik.add(InlineKeyboardButton("✅Получить эксель", callback_data=cb_main.new(action="get_table")))
    ik.add(InlineKeyboardButton("Удалить товар", callback_data=cb_main.new(action="delete_item")))
    ik.add(InlineKeyboardButton("❌Отменить", callback_data=cb_main.new(action="main")))
           
    return ik