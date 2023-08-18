from loguru import logger

import asyncio
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import concurrent.futures
from aiogram.utils import executor
from pandas import ExcelWriter

from create_bot import dp, bot
from keyboards import client_k
from foxypost import PostStatAggregator
import pandas as pd
from aiogram.types import InputFile

logger.add("logs.log", format="{time} {level} {message} {name}", level="DEBUG")

class FSMvib(StatesGroup):
    soc_net = State()
    link = State()

async def get_youtube(callback:types.CallbackQuery,state:FSMContext):
    async with state.proxy() as soc_net:
        soc_net["soc_net"] = callback.data.split('_')[1]
    kap = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    cnopka_start = types.KeyboardButton("Отмена")
    kap.add(cnopka_start)
    await FSMvib.next()
    await bot.send_message(callback.message.chat.id,"""Отправь ссылки на shorts в формате https://www.youtube.com/shorts/nDlAoNEbNdI""",
                                  reply_markup=kap)

async def get_link_youtube(message: types.message, state:FSMContext) -> str:
    try:
        loop = asyncio.get_running_loop()

        async with state.proxy() as link:
            link["link"] = message.text
            aggregator = PostStatAggregator(social_network="youtube", collection_link=[link["link"]],options = [])

        await state.finish()
        await bot.send_message(message.chat.id, "Данные собираются📂 Пожалуйста, подождите..",
                               reply_markup=client_k.coll_service)
        with concurrent.futures.ThreadPoolExecutor() as pool:
            data = await loop.run_in_executor(
                pool, aggregator.get_data)

        await bot.send_message(message.chat.id, data,
                                   reply_markup=client_k.coll_service)
    except Exception as f:
        logger.warning(f)

def register_handlers_youtube(dp:Dispatcher):
    dp.register_callback_query_handler(get_youtube, Text(startswith="soc_youtube"), state=None)
    dp.register_message_handler(get_link_youtube, state=FSMvib.soc_net)