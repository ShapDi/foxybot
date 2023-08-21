import os
import time

import asyncio
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import concurrent.futures
from loguru import logger

from create_bot import dp, bot
from keyboards import client_k
from foxypost import PostStatAggregator
import pandas as pd

logger.add("logs.log", format="{time} {level} {message} {name}", level="ERROR")

class FSMyoutube(StatesGroup):
    soc_net = State()
    link = State()

async def get_youtube(callback:types.CallbackQuery,state:FSMContext):
    async with state.proxy() as soc_net:
        soc_net["soc_net"] = callback.data.split('_')[1]
    kap = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    cnopka_start = types.KeyboardButton("Отмена")
    kap.add(cnopka_start)
    await  FSMyoutube.next()
    await bot.send_message(callback.message.chat.id,"""Отправь ссылки на shorts""",
                                  reply_markup=kap)

async def get_link_youtube(message: types.message, state:FSMContext) -> str:
    try:
        loop = asyncio.get_running_loop()

        async with state.proxy() as link:
            link["link"] = message.text.split("\n")
            aggregator = PostStatAggregator(social_network="youtube", collection_link=link["link"],options = [])
        await state.finish()
        await bot.send_message(message.chat.id, "Данные собираются📂 Пожалуйста, подождите..",
                               reply_markup=client_k.coll_service)
        with concurrent.futures.ThreadPoolExecutor() as pool:
            data = await loop.run_in_executor(
                pool, aggregator.get_data)
        name_table = f"data_{str(time.time()).split('.')[0]}"

        df = pd.DataFrame({"link": [(list(x.keys())[0]) for x in data],
                               "play_count": [
                                   (str(list(x.values())[0])).split(" ")[1].replace("viewCount:", "").replace("'","").replace(",", "") for x in data],
                               "commentCount": [
                                   (str(list(x.values())[0])).split(" ")[3].replace("commentCount:", "").replace("'","").replace(",", "") for x in data],
                               "likeCount": [
                                   ((str(list(x.values())[0])).split(" "))[5].replace("likeCount:", "").replace("'","").replace(",", "") for x in
                                   data],
                               "data": [((str(list(x.values())[0])).split(" "))[7].replace("data:", "").replace("'",
                                                                                                                "").replace(
                                   "}", "") for x in
                                        data]})
        df.to_excel(f'{name_table}.xlsx')

        await bot.send_document(message.chat.id, document=open(f'{name_table}.xlsx', "rb"))
        os.remove(f'{name_table}.xlsx')
    except Exception as f:
        logger.error(f)

def register_handlers_youtube(dp:Dispatcher):
    dp.register_callback_query_handler(get_youtube, Text(startswith="soc_youtube"), state=None)
    dp.register_message_handler(get_link_youtube, state= FSMyoutube.soc_net)