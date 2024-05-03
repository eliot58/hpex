from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot.common import cb_main
from bot.states import RegisterStates, TrackStates, RansomStates
from bot.keyboards import fill_address_kb, main_keyboard, is_correct_ik, back_to_main_kb
from bot.utils import generate_code, validate_phone_number
from bot.api import create_client, get_texts
from bot.create_bot import bot

async def register(call: types.CallbackQuery, state: FSMContext):
    texts = await get_texts()
    await state.set_state(RegisterStates.full_name_input)
    await call.message.answer(texts[17]["text"])

async def control_table(call: types.CallbackQuery, state: FSMContext):
    texts = await get_texts()
    await state.set_state(TrackStates.code_input)
    await call.message.answer(texts[18]["text"])

async def ransom(call: types.CallbackQuery, state: FSMContext):
    texts = await get_texts()
    await state.set_state(RansomStates.code_input)
    await call.message.answer(texts[18]["text"])

async def fill_address(call: types.CallbackQuery):
    texts = await get_texts()
    await call.message.answer(texts[19]["text"], reply_markup=fill_address_kb())

async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    texts = await get_texts()
    await state.set_state("*")
    await state.reset_state()
    await call.message.answer(texts[20]["text"], reply_markup=main_keyboard())


async def full_name_input(message: types.Message, state: FSMContext):
    texts = await get_texts()
    await state.update_data(full_name=message.text)
    await state.set_state(RegisterStates.phone_input)
    await message.answer(texts[21]["text"])

async def phone_input(message: types.Message, state: FSMContext):
    texts = await get_texts()
    if validate_phone_number(message.text):
        await state.update_data(phone=message.text)
        await state.set_state(RegisterStates.city_input)
        await message.answer(texts[22]["text"])
    else:
        await message.answer(texts[8]["text"])

async def city_input(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.update_data(code="KF-"+generate_code())
    data = await state.get_data()
    text = f"Данные клиента :\n\n"\
            f"Код клиента: {data['code']}\n"\
            f"ФИО: {data['full_name']}\n"\
            f"Номер телефона: {data['phone']}\n"\
            f"Город: {data['city']}\n"
    await message.answer(text, reply_markup=is_correct_ik())

async def is_correct(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await create_client(user_id=call.message.chat.id, full_name=data["full_name"], code=data["code"],\
                        city=data["city"], phone=data["phone"])

    registartion_text = "Спасибо за регистрацию, мы рады с вами сотрудничать ❤️\n\n"\
                        "<b>Вот данные для выкупа вашего товара на наш склад:</b>\n" \
                        f"Клиентский код : <code>{data['code']}</code>\n"\
                        f"Имя получателя : {data['code']}\n"\
                        "Номер получателя : <code>18664541313</code>\n"\
                        "Индекс : <code>510180</code>\n"\
                        "Адрес : <code>广东省 佛山市 南海区 矿泉街道</code>\n"\
                        f"Комментарий : <code>荔德路318号汇富商贸中心 A7-103 {data['code']}</code>"
    

    text = f"Данные клиента :\n\n"\
            f"Код клиента: {data['code']}\n"\
            f"ФИО: {data['full_name']}\n"\
            f"Номер телефона: {data['phone']}\n"\
            f"Город: {data['city']}\n"
    await bot.send_message(-1002015553544, text)
    
    
    await call.message.answer(registartion_text, reply_markup=back_to_main_kb())

async def is_not_correct(call: types.CallbackQuery, state: FSMContext):
    texts = await get_texts()
    await state.set_state(RegisterStates.full_name_input)
    await call.message.answer(texts[16]["text"])

def register_main(dp: Dispatcher):

    dp.register_callback_query_handler(register, cb_main.filter(action="register"), state="*")
    dp.register_callback_query_handler(control_table, cb_main.filter(action="control_table"), state="*")
    dp.register_callback_query_handler(ransom, cb_main.filter(action="ransom"), state="*")
    dp.register_callback_query_handler(fill_address, cb_main.filter(action="fill_address"), state="*")
    dp.register_callback_query_handler(back_to_main, cb_main.filter(action="main"), state="*")

    dp.register_message_handler(full_name_input, commands=None, content_types=types.ContentTypes.TEXT, state=RegisterStates.full_name_input)
    dp.register_message_handler(phone_input, commands=None, content_types=types.ContentTypes.TEXT, state=RegisterStates.phone_input)
    dp.register_message_handler(city_input, commands=None, content_types=types.ContentTypes.TEXT, state=RegisterStates.city_input)
    dp.register_callback_query_handler(is_correct, cb_main.filter(action="is_correct"), state=RegisterStates.city_input)
    dp.register_callback_query_handler(is_not_correct, cb_main.filter(action="is_not_correct"), state=RegisterStates.city_input)
