import logging
from aiogram import types

from create_bot import bot, logs_path
from configs.smth import ADMINS


async def error_occured(message: types.Message):
    logging.exception("The traceback of the ERROR:")

    await message.answer("Извини, что-то пошло не так(\nМы уже получили ошибку, разберемся!\nЕсли долго не чиним, можешь написать @Madfyre и/или @vbalab по поводу бота.")

    for admin in ADMINS:
        await bot.send_message(admin, f"Error, check the logs. User: @{message.from_user.username}. Message: \"{message.text}\"")


async def send_logs():
    for admin in ADMINS:
        await bot.send_message(admin, "Bot has finished working!")
        await bot.send_document(admin, document=types.FSInputFile(logs_path))
