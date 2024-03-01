from aiogram import types

from create_bot import bot
from configs.smth import ADMINS


async def send_error_message(message: types.Message):
    await message.answer("Извини, что-то пошло не так(\nМы уже получили ошибку, разберемся!\nЕсли долго не чиним, можешь написать @Madfyre и/или @vbalab по поводу бота.")

    for admin in ADMINS:
        await bot.send_message(admin, f"FUCK, error, check the logs. User: @{message.from_user.username}. Message: \"{message.text}\"")
