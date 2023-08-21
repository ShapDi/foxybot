from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage=MemoryStorage()

TOK="6665421623:AAGCMaQDWOxGyCmrc8hseNqaR-PtBW3c56s"
bot = Bot(token=TOK)
dp=Dispatcher(bot, storage=storage)

