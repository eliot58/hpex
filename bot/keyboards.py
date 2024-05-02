import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from .common import cb_main
from .api import get_buttons

buttons = []

async def main():
    global buttons 
    buttons = await get_buttons()

def phone_tied_kb():
    rp = ReplyKeyboardMarkup(resize_keyboard=True)
    rp.add(KeyboardButton(buttons[2]["text"]), KeyboardButton(buttons[3]["text"]))
    return rp

def is_correct_rb():
    rp = ReplyKeyboardMarkup(resize_keyboard=True)
    rp.add(KeyboardButton(buttons[0]["text"]), KeyboardButton(buttons[1]["text"]))
    return rp

def is_correct_ik():
    ik = InlineKeyboardMarkup()
    ik.add(InlineKeyboardButton(buttons[0]["text"], callback_data=cb_main.new(action="is_correct")), InlineKeyboardButton(buttons[1]["text"], callback_data=cb_main.new(action="is_not_correct")))
           
    return ik


def qr_code_kb():
    rp = ReplyKeyboardMarkup(resize_keyboard=True)
    rp.add(KeyboardButton(buttons[4]["text"]))
    return rp


def main_keyboard():
    ik = InlineKeyboardMarkup()
    ik.add(InlineKeyboardButton(buttons[13]["text"], url="https://t.me/Georg_opt2"), 
           InlineKeyboardButton(buttons[14]["text"], callback_data=cb_main.new(action="control_table")))
    ik.add(InlineKeyboardButton(buttons[15]["text"], callback_data=cb_main.new(action="ransom")),
           InlineKeyboardButton(buttons[16]["text"], callback_data=cb_main.new(action="fill_address")))
    ik.add(InlineKeyboardButton(buttons[17]["text"], callback_data=cb_main.new(action="register")))
           
           
    return ik

def back_to_main_kb():
    ik = InlineKeyboardMarkup()
    ik.add(InlineKeyboardButton(buttons[5]["text"], callback_data=cb_main.new(action="main")))
           
    return ik

def fill_address_kb():
    ik = InlineKeyboardMarkup()
    ik.add(InlineKeyboardButton(buttons[8]["text"], callback_data=cb_main.new(action="factory")))
    ik.add(InlineKeyboardButton(buttons[9]["text"], callback_data=cb_main.new(action="1688")))
    ik.add(InlineKeyboardButton(buttons[10]["text"], callback_data=cb_main.new(action="pinduo")))
    ik.add(InlineKeyboardButton(buttons[11]["text"], callback_data=cb_main.new(action="poizon")))
    ik.add(InlineKeyboardButton(buttons[12]["text"], callback_data=cb_main.new(action="taobao")))
    ik.add(InlineKeyboardButton(buttons[5]["text"], callback_data=cb_main.new(action="main")))
           
    return ik

def table_keyboard():
    ik = InlineKeyboardMarkup()
    ik.add(InlineKeyboardButton(buttons[6]["text"], callback_data=cb_main.new(action="get_table")))
    ik.add(InlineKeyboardButton(buttons[7]["text"], callback_data=cb_main.new(action="delete_item")))
    ik.add(InlineKeyboardButton(buttons[5]["text"], callback_data=cb_main.new(action="main")))
           
    return ik


asyncio.run(main())