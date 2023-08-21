from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage=MemoryStorage()

TOK=""
bot = Bot(token=TOK)
dp=Dispatcher(bot, storage=storage)

