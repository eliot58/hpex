from aiogram import types, Dispatcher
from bot.common import cb_main
from aiogram.types import InputFile
from bot.keyboards import back_to_main_kb
from bot.api import get_agent_by_id

async def pinduo(call: types.CallbackQuery):
    agent = await get_agent_by_id(call.message.chat.id)
    text = "Инструкции для Pinduoduo:\n\n"\
            f"1 - Код клиента: {agent[0]['code']} \n"\
            "2 - Номер получателя: 18664541313\n"\
            "3 - Адрес: 广东省广州市 越秀区\n"\
            f"4 - Комментарий: 荔德路318号汇富商贸中心 A7-103 {agent[0]['code']}"
    await call.message.answer_photo(InputFile("instructions/pinduo.jpg"), text, reply_markup=back_to_main_kb())

async def taobao(call: types.CallbackQuery):
    agent = await get_agent_by_id(call.message.chat.id)
    text = "Инструкции для TaoBao:\n\n"\
            f"1 - Код клиента: {agent[0]['code']}\n"\
            "2 - Номер получателя: 18664541313\n"\
            "3 - Адрес: 广东省广州市 越秀区 矿泉街道\n"\
            f"4 - Комментарий: 荔德路318号汇富商贸中心 A7-103 {agent[0]['code']}"
    await call.message.answer_photo(InputFile("instructions/taobao.jpg"), text, reply_markup=back_to_main_kb())

async def poizon(call: types.CallbackQuery):
    agent = await get_agent_by_id(call.message.chat.id)
    text = "Инструкции для Poizon \n\n:"\
            f"1 - Код клиента: {agent[0]['code']}\n"\
            "2 - Номер получателя: 18664541313\n"\
            "3 - Адрес: 广东省广州市 越秀区 矿泉街道\n"\
            f"4 - Комментарий: 荔德路318号汇富商贸中心 A7-103 {agent[0]['code']}"
    await call.message.answer_photo(InputFile("instructions/poizon.jpg"), text, reply_markup=back_to_main_kb())

async def m1688(call: types.CallbackQuery):
    agent = await get_agent_by_id(call.message.chat.id)
    text = "Инструкции для 1688:\n\n"\
            f"1 - Код клиента: {agent[0]['code']}\n"\
            "2 - Номер получателя: 18664541313\n"\
            "3 - Индекс: 510180\n"\
            "4 - Адрес: 广东省广州市 越秀区 矿泉街道\n"\
            f"5 - Комментарий: 荔德路318号汇富商贸中心 A7-103 {agent[0]['code']}"
    await call.message.answer_photo(InputFile("instructions/m1688.jpg"), text, reply_markup=back_to_main_kb())

async def factory(call: types.CallbackQuery):
    agent = await get_agent_by_id(call.message.chat.id)
    text = "Инструкция для фабрики: \n\n"\
            f"收货人: {agent[0]['code']}\n"\
            "电话: 18664541313\n"\
            f"广东省广州市越秀区荔德路318号汇富商贸中心A7-103 {agent[0]['code']}\n\n"\
            "Скопировать и отправить Китайцам."
    await call.message.answer(text, reply_markup=back_to_main_kb())

def register_address(dp: Dispatcher):
    dp.register_callback_query_handler(pinduo, cb_main.filter(action="pinduo"), state="*")
    dp.register_callback_query_handler(factory, cb_main.filter(action="factory"), state="*")
    dp.register_callback_query_handler(m1688, cb_main.filter(action="1688"), state="*")
    dp.register_callback_query_handler(poizon, cb_main.filter(action="poizon"), state="*")
    dp.register_callback_query_handler(taobao, cb_main.filter(action="taobao"), state="*")