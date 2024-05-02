from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot.common import cb_main
from bot.states import RansomStates
from bot.keyboards import table_keyboard, main_keyboard
from bot.utils import validate_code
from bot.table import generate_ransom
from bot.api import get_client, get_agent_by_code, create_ransom, get_texts
from aiogram.types import InputFile


async def code_input(message: types.Message, state: FSMContext):
    texts = await get_texts()
    if validate_code(message.text.upper()):
        client = (await get_client(message.text.upper())) or (await get_agent_by_code(message.text.upper()))
        if client:
            await state.update_data(client_code=message.text.upper())
            await state.set_state(RansomStates.items_upload)
            await message.answer(texts[23]["text"])
        else:
            await message.answer(texts[24]["text"])
    else:
        await message.answer(texts[25]["text"])


async def items_upload(message: types.Message, state: FSMContext):
    texts = await get_texts()
    data = await state.get_data()
    products = data.get('products', [])
    async def process_photo(photo_message):
        caption = photo_message.caption
        if caption:
            check_caption = caption.split(",")
            if len(check_caption) == 4:
                link, comment, quantity, price = check_caption
                if quantity.isdigit():
                    photo = await photo_message.photo[-1].download()

                    products.append([photo.name, link, comment, quantity, price])
                    await state.update_data(products=products,
                                            count=data.get('count', 0) + 1)
                    await message.answer(f'Товар #{data.get("count", 0)} успешно сохранён. Если нужно больше фото, то отправьте фото с подписью. '
                                        'Либо нажмите на кнопку, чтобы сформировать эксель документ', reply_markup=table_keyboard())
                else:
                    await message.answer(texts[26]["text"])
            else:
                await message.answer(texts[26]["text"])
        else:
            await message.answer(texts[27]["text"])


    if message.photo:
        await process_photo(message)
    elif message.document and message.document.mime_type.startswith('image/'):
        await process_photo(message)
    else:
        await message.answer(texts[28]["text"])


async def get_table(call: types.CallbackQuery, state: FSMContext):
    texts = await get_texts()
    data = await state.get_data()
    if data.get('count'):
        await call.message.answer(texts[29]["text"])

        table = generate_ransom(data["client_code"], data["products"])

        await create_ransom(table)

        await call.message.answer_document(InputFile(table))


        await call.message.answer(texts[30]["text"],
                                reply_markup=main_keyboard())
        await state.reset_state()
    else:
        await call.message.answer(texts[31]["text"])
        
async def delete_item(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(RansomStates.delete_input)
    products = data.get('products', [])
    await call.message.answer(
            f'Пришлите порядковый номер товара. Сейчас последний товар с порядковым номером {len(products)}:')
    
async def delete_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    products = data.get('products', [])

    try:
        index = int(message.text)
        if 0 < index <= len(products):
            true_index = index - 1
            products.pop(true_index)
            await message.answer(f"Товар с индексом {index} удален. Теперь отправьте фото в формате: ФОТО + ПОДПИСЬ "
                                 f"(Трек_код.комментарий.количество). Пример подписи: 7212.Серый 24 27 28.3",
                                 reply_markup=table_keyboard())
            await state.update_data({'products': products})
            await state.set_state(RansomStates.items_upload)
        else:
            await message.answer(f"Некорректный индекс. Пожалуйста, укажите правильный индекс, который будет больше "
                                 f"чем 0 и меньше или равным {len(products)}")
    except ValueError:
        await message.answer(f"Некорректное число. Пожалуйста, введите целое число, которое будет больше "
                             f"чем 0 и меньше или равным {len(products)}")

def register_ransom(dp: Dispatcher):
    dp.register_message_handler(code_input, commands=None, content_types=types.ContentTypes.TEXT, state=RansomStates.code_input)
    dp.register_message_handler(items_upload, commands=None, content_types=types.ContentTypes.PHOTO, state=RansomStates.items_upload)
    dp.register_callback_query_handler(get_table, cb_main.filter(action="get_table"), state=RansomStates.items_upload)
    dp.register_callback_query_handler(delete_item, cb_main.filter(action="delete_item"), state=RansomStates.items_upload)
    dp.register_message_handler(delete_input, commands=None, content_types=types.ContentTypes.TEXT, state=RansomStates.delete_input)