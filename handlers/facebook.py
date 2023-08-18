from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text

from keyboards import client_k

async def get_face(callback:types.CallbackQuery,state:FSMContext):
    async with state.proxy() as soc_net:
        soc_net["soc_net"] = callback.data.split('_')[1]
    await bot.send_message(chat_id=callback.message.chat.id, text="В разработке")

async def FSMstop(message:types.Message, state:FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await message.reply("ОК", reply_markup=client_k.coll_service)

def register_handlers_facebook(dp: Dispatcher):
    dp.register_callback_query_handler(get_face, Text(startswith="soc_facebook"), state=None)
    dp.register_message_handler(FSMstop, Text(equals="Отмена", ignore_case=True), state="*")