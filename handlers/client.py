import asyncio
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from keyboards import client_k



async def bot_message(message: types.Message):
    await bot.send_message(message.chat.id,"""Привет👋\n
Данный бот предназначен для быстрого доступа к различным сервисам компании. На данный момент разработаны следующие сервисы:\n
1️⃣Статистика публикаций из соцсетей
Сервис позволяет получать данные с постов и видео из различных соцсетей\n
Выбирай нужный сервис по кнопке ниже⬇️""",reply_markup=client_k.coll_service )

async def get_social_network(message: types.Message):
    await message.answer("""Статистика публикаций из соцсетей\n
Данный сервис позволяет получать данные с постов и видео из различных соцсетей📊\n
Данные выгружаются в текстовом формате + файлом Excel.\n
Выбери соцсеть, из которой будут собираться данные🗂""", reply_markup=client_k.nabor_soc)

async def FSMstop(message:types.Message, state:FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await message.reply("ОК", reply_markup=client_k.coll_service)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(bot_message, commands=["start"]),
    dp.register_message_handler(get_social_network, text=["Статистика публикаций из соцсетей"],state=None)
    dp.register_message_handler(FSMstop, Text(equals="Отмена", ignore_case=True), state="*")






