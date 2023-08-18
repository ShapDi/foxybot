from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

service_one = KeyboardButton(text="Статистика публикаций из соцсетей")
coll_service = ReplyKeyboardMarkup(resize_keyboard=True)
coll_service.add(service_one)


# facebook = InlineKeyboardButton(text="facebook",callback_data="soc_facebook")
instagram = InlineKeyboardButton(text="instagram",callback_data="soc_instagram")
youtube = InlineKeyboardButton(text="youtube",callback_data="soc_youtube")
nabor_soc = InlineKeyboardMarkup(row_width=1)
nabor_soc.add(instagram,youtube)