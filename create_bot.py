import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')

storage=MemoryStorage()

TOK=token
bot = Bot(token=TOK)
dp=Dispatcher(bot, storage=storage)

