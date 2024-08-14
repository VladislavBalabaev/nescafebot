from aiogram import types

from create_bot import bot
from configs.logs import logs_path
from configs.selected_ids import ADMINS


async def send_startup():
    for admin in ADMINS:
        await bot.send_message(admin, "Bot has started working!")


async def send_shutdown():
    for admin in ADMINS:
        await bot.send_message(admin, "Bot has finished working!")
        await bot.send_document(admin, document=types.FSInputFile(logs_path))
