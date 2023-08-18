from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage=MemoryStorage()

TOK="5690500950:AAG9UfkPxd9tGF1RaYjwP27npv0ri5jYt4k"
bot = Bot(token=TOK)
dp=Dispatcher(bot, storage=storage)

