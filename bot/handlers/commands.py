from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from bot.states import FormStates
from bot.keyboards import main_keyboard
from bot.create_bot import bot
from bot.api import get_texts, get_agent_by_id
from random import uniform
import asyncio


async def cmd_start(message: types.Message, state: FSMContext):
    agent = await get_agent_by_id(message.chat.id)

    if not agent:
        await state.set_state(FormStates.full_name_input)
        text = 'Для пользования ботом необходимо пройти простую регистрацию. Для этого нужно последовательно ответить ' \
                'на несколько вопросов нашего бота.\n\nДля начала введите свои данные ФИО или данные получателя: '
        await message.answer(text)
    else:
        start_texts = await get_texts()
        await state.set_state("*")
        for text in start_texts[:-1]:
            await message.answer(text["text"])
            await bot.send_chat_action(message.chat.id, 'typing')
            await asyncio.sleep(uniform(1, 3))

        fin_text = start_texts[-1]["text"]
        await message.answer(fin_text, reply_markup=main_keyboard())


def register_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")