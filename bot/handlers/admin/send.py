from aiogram import types

from bot.configs.admin_ids import ADMINS
from create_bot import bot, logs_path


async def send_startup():
    for admin in ADMINS:
        await bot.send_message(admin, "Bot has started working!")


async def send_shutdown():
    for admin in ADMINS:
        await bot.send_message(admin, "Bot has finished working!")
        await bot.send_document(admin, document=types.FSInputFile(logs_path))
