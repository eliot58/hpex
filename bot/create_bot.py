from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(os.getenv('BOT'), parse_mode="HTML")