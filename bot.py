from aiogram.utils import executor
from create_bot import dp
from handlers import client, instagram, facebook

from threading import Thread

async def on_start():
    print("bot start")

instagram.register_handlers_instagram(dp)
client.register_handlers_client(dp)
facebook.register_handlers_facebook(dp)



executor.start_polling(dp)
