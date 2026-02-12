from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

#
# def main_menu():
#     builder = ReplyKeyboardBuilder()
#     builder.row(
#         types.KeyboardButton(text="☁️ Cloud"),
#         types.KeyboardButton(text="🎧 Shazam")
#     )
#     return builder.as_markup(resize_keyboard=True)


def format_selector():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="1080p 🔥", callback_data="dl_1080"),
        types.InlineKeyboardButton(text="720p ✅", callback_data="dl_720")
    )
    builder.row(
        types.InlineKeyboardButton(text="480p ⚡", callback_data="dl_480"),
        types.InlineKeyboardButton(text="360p 📉", callback_data="dl_360")
    )
    builder.row(
        types.InlineKeyboardButton(text="🎵 MP3", callback_data="dl_audio")
    )
    return builder.as_markup()
