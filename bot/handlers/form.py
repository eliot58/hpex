from aiogram import types, Dispatcher
from bot.states import FormStates
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from bot.keyboards import phone_tied_kb, is_correct_rb, qr_code_kb, main_keyboard
from bot.create_bot import bot
from bot.api import create_agent, get_texts
from bot.utils import generate_code, is_valid_date, validate_phone_number


async def full_name_input(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(FormStates.date_of_birth_input)
    texts = await get_texts()
    await message.answer(texts[5]["text"])

async def date_input(message: types.Message, state: FSMContext):
    texts = await get_texts()
    if is_valid_date(message.text):
        await state.update_data(date_of_birth=message.text)
        await state.set_state(FormStates.phone_input)
        await message.answer(texts[6]["text"])
    else:
        await message.answer(texts[7]["text"])

async def phone_input(message: types.Message, state: FSMContext):
    texts = await get_texts()
    if validate_phone_number(message.text):
        await state.update_data(phone=message.text)
        await state.set_state(FormStates.phone_tied)
        await message.answer(f"Номер телефона {message.text} привязан к телеграмму получателя?", reply_markup=phone_tied_kb())
    else:
        await message.answer(texts[8]["text"])

async def phone_tied(message: types.Message, state: FSMContext):
    texts = await get_texts()
    if message.text == "Привязан":
        await state.update_data(username=None)
        await state.set_state(FormStates.city_input)
        await message.answer(texts[9]["text"], reply_markup=ReplyKeyboardRemove())
    elif message.text == "Не привязан":
        await state.set_state(FormStates.username_input)
        text = texts[10]["text"]
        await message.answer(text, reply_markup=ReplyKeyboardRemove())


async def username_input(message: types.Message, state: FSMContext):
    texts = await get_texts()
    await state.update_data(username=message.text)
    await state.set_state(FormStates.city_input)
    await message.answer(texts[9]["text"])


async def city_input(message: types.Message, state: FSMContext):
    texts = await get_texts()
    await state.update_data(city=message.text)
    await state.set_state(FormStates.transport_input)
    await message.answer(texts[11]["text"])


async def transport_input(message: types.Message, state: FSMContext):
    texts = await get_texts()
    await state.update_data(transport=message.text)
    await state.set_state(FormStates.qr_code_input)
    await message.answer(texts[12]["text"], reply_markup=qr_code_kb())

async def upload_photo(message: types.Message, state: FSMContext):
    texts = await get_texts()
    await state.update_data(photo=message.photo)
    await state.update_data(code="KF-"+generate_code())
    await state.set_state(FormStates.submit_form)
    data = await state.get_data()
    text = f"Данные клиента :\n\n"\
        f"Код: {data['code']}\n"\
        f"ФИО: {data['full_name']}\n"\
        f"ДР: {data['date_of_birth']}\n"\
        f"Номер телефона: {data['phone']}\n"\
        f"Телеграмм: {data['username'] if data['username'] else data['phone']}\n"\
        f"Город: {data['city']}\n"\
        f"Адрес доставки (ТК): {data['transport']}\n"
    await message.answer(texts[13]["text"])
    await message.answer_photo(photo=data["photo"][-1].file_id, caption = text, reply_markup=is_correct_rb())


async def not_qr_code(message: types.Message, state: FSMContext):
    texts = await get_texts()
    await state.update_data(photo=None)
    await state.update_data(code="KF-"+generate_code())
    await state.set_state(FormStates.submit_form)
    data = await state.get_data()
    text = f"Данные клиента :\n\n"\
        f"Код: {data['code']}\n"\
        f"ФИО: {data['full_name']}\n"\
        f"ДР: {data['date_of_birth']}\n"\
        f"Номер телефона: {data['phone']}\n"\
        f"Телеграмм: {data['username'] if data['username'] else data['phone']}\n"\
        f"Город: {data['city']}\n"\
        f"Адрес доставки (ТК): {data['transport']}\n"
    await message.answer(texts[13]["text"])
    await message.answer(text, reply_markup=is_correct_rb())

async def is_correct(message: types.Message, state: FSMContext):
    texts = await get_texts()
    if message.text == "Всё верно":
        data = await state.get_data()

        if data["photo"]:
            qr_code = (await data["photo"][-1].download()).name
        else:
            qr_code = None

        await create_agent(message.chat.id, full_name=data["full_name"], date_of_birth=data["date_of_birth"],\
                           city=data["city"], transport=data["transport"], username=data["username"], phone=data["phone"],\
                            code=data["code"], qr_code=qr_code)
        
        text = f"Данные клиента :\n\n"\
            f"Код: {data['code']}\n"\
            f"ФИО: {data['full_name']}\n"\
            f"ДР: {data['date_of_birth']}\n"\
            f"Номер телефона: {data['phone']}\n"\
            f"Телеграмм: {data['username'] if data['username'] else data['phone']}\n"\
            f"Город: {data['city']}\n"\
            f"Адрес доставки (ТК): {data['transport']}\n"
        if data["photo"]:
            await bot.send_photo(977794713, data["photo"][-1].file_id, text)
        else:
            await bot.send_message(977794713, text)
        await state.set_state("*")
        await message.answer(texts[14]["text"], reply_markup=ReplyKeyboardRemove())
        await message.answer(texts[15]["text"], reply_markup=main_keyboard())
    elif message.text == "Нет исправить":
        await state.set_state(FormStates.full_name_input)
        await message.answer(texts[16]["text"], reply_markup=ReplyKeyboardRemove())


def register_form(dp: Dispatcher):
    dp.register_message_handler(full_name_input, commands=None, content_types=types.ContentTypes.TEXT, state=FormStates.full_name_input)
    dp.register_message_handler(date_input, commands=None, content_types=types.ContentTypes.TEXT, state=FormStates.date_of_birth_input)
    dp.register_message_handler(phone_input, commands=None, content_types=types.ContentTypes.TEXT, state=FormStates.phone_input)
    dp.register_message_handler(username_input, commands=None, content_types=types.ContentTypes.TEXT, state=FormStates.username_input)
    dp.register_message_handler(phone_tied, commands=None, content_types=types.ContentTypes.TEXT, state=FormStates.phone_tied)
    dp.register_message_handler(city_input, commands=None, content_types=types.ContentTypes.TEXT, state=FormStates.city_input)
    dp.register_message_handler(transport_input, commands=None, content_types=types.ContentTypes.TEXT, state=FormStates.transport_input)
    dp.register_message_handler(upload_photo, commands=None, content_types=types.ContentTypes.PHOTO, state=FormStates.qr_code_input)
    dp.register_message_handler(not_qr_code, commands=None, content_types=types.ContentTypes.TEXT, state=FormStates.qr_code_input)
    dp.register_message_handler(is_correct, commands=None, content_types=types.ContentTypes.TEXT, state=FormStates.submit_form)