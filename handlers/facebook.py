from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text

from keyboards import client_k

async def get_face(callback:types.CallbackQuery,state:FSMContext):
    async with state.proxy() as soc_net:
        soc_net["soc_net"] = callback.data.split('_')[1]
    await bot.send_message(chat_id=callback.message.chat.id, text="В разработке")

def register_handlers_facebook(dp: Dispatcher):
    dp.register_callback_query_handler(get_face, Text(startswith="soc_facebook"), state=None)