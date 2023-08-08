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
from singlepostscraper import PostStatAggregator
import pandas as pd
from aiogram.types import InputFile



class FSMvib(StatesGroup):
    soc_net = State()
    link = State()
    login = State()
    password = State()

async def get_inst(callback:types.CallbackQuery,state:FSMContext):
    async with state.proxy() as soc_net:
        soc_net["soc_net"] = callback.data.split('_')[1]
    kap = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    cnopka_start = types.KeyboardButton("Отмена")
    kap.add(cnopka_start)
    await FSMvib.next()
    await bot.send_message(callback.message.chat.id,"""Для пакетной обработки постов и рилсов их необходимо собрать в сохраненках (Saved) в Instagram в отдельную папку💾\n\nПосле сбора публикаций, необходимо скопировать ссылку на папку в Saved (сделать это можно через браузерную версию сайта с телефона или компьютера).""",
                                  reply_markup=kap)


async def get_link(message: types.message, state:FSMContext) -> str:
    async with state.proxy() as st:
        st["link"] = message.text
    await FSMvib.next()
    await bot.send_message(message.chat.id,"Отправьте логин от аккаунта Instagram (вход в аккаунт нужен для просмотра сохраненных постов и рилсов, данные не сохраняются✖️)")


async def get_login(message: types.message, state:FSMContext):
    async with state.proxy() as st:
        st["login"] = message.text
    await bot.send_message(message.chat.id, "Отправьте пароль от аккаунта Instagram (вход в аккаунт нужен для просмотра сохраненных постов и рилсов, данные не сохраняются✖️)")
    await FSMvib.next()


async def get_password(message:types.Message, state:FSMContext):
    loop = asyncio.get_running_loop()
    async with state.proxy() as st:
        st["password"] = message.text
        options = {"instagram": {"usеrname": f"{st['login']}", "password": f"{st['password']}"}}
        fun = PostStatAggregator(social_network="instagram",collection_link=st['link'], options=options)
    await state.finish()
    await bot.send_message(message.chat.id,"Данные собираются📂 Пожалуйста, подождите..", reply_markup=client_k.coll_service)
    with concurrent.futures.ThreadPoolExecutor() as pool:
        data = await loop.run_in_executor(
            pool, fun.get_data)
    if len(data)<20:
        text = str(data).replace("}", "").replace("{", "").replace("[", "").replace("]", "").replace("'play_count","\n'play_count'")
        await bot.send_message(message.from_user.id,text=text, reply_markup=client_k.coll_service)
    try:
            df = pd.DataFrame({"link": [(list(x.keys())[0]) for x in data],
                               "play_count": [(str(list(x.values())[0])).split(" ")[0].replace("play_count:","") for x in data],
                               "comment_count":[(str(list(x.values())[0])).split(" ")[1].replace("comment_count:","") for x in data],
                               "like_count":[((str(list(x.values())[0])).split(" "))[2].replace("like_count:","") for x in data]})
            df.to_excel('data.xlsx')
            await bot.send_document(message.chat.id,document=open('data.xlsx', "rb"))
    except Exception as f:
        print(f)







async def FSMstop(message:types.Message, state:FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await message.reply("ОК", reply_markup=client_k.coll_service)


def register_handlers_instagram(dp:Dispatcher):
    dp.register_callback_query_handler(get_inst, Text(startswith="soc_instagram"), state=None)
    dp.register_message_handler(FSMstop, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(get_link, state=FSMvib.soc_net)
    dp.register_message_handler(get_login, state=FSMvib.link)
    dp.register_message_handler(get_password, state=FSMvib.login)



