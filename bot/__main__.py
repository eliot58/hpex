import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.handlers.commands import register_commands
from bot.handlers.form import register_form
from bot.handlers.main_handlers import register_main
from bot.handlers.track import register_track
from bot.handlers.ransom import register_ransom
from bot.handlers.address import register_address
from dotenv import load_dotenv

load_dotenv()


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(os.getenv('BOT'), parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_commands(dp)
    register_form(dp)
    register_main(dp)
    register_track(dp)
    register_ransom(dp)
    register_address(dp)


    await dp.start_polling()

try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logging.error("Bot stopped!")