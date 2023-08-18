from aiogram.utils import executor
from create_bot import dp
from handlers import client,instagram,facebook,youtube

from threading import Thread

async def on_start():
    print("bot start")

client.register_handlers_client(dp)
youtube.register_handlers_youtube(dp)
instagram.register_handlers_instagram(dp)
facebook.register_handlers_facebook(dp)



executor.start_polling(dp)
