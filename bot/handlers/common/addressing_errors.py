import logging
from aiogram import types
from functools import wraps

from configs.selected_ids import ADMINS
from create_bot import bot


async def error_occured(message: types.Message, e: Exception):
    logging.exception("The traceback of the ERROR:")

    await message.answer("Извини, что-то пошло не так(\nМы уже получили ошибку, разберемся!\nЕсли долго не чиним, можешь написать @Madfyre и/или @vbalab по поводу бота.")

    for admin in ADMINS:
        await bot.send_message(admin, f"Error, check the logs.\nUser: @{message.from_user.username}. Message: \"{message.text}\".\n\n{e.__class__.__name__ }: {e}")


def error_sender(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            await f(*args, **kwargs)

        except Exception as e:
            if "message" in kwargs.keys():
                await error_occured(kwargs["message"], e)
            else:
                for arg in args:
                    if type(arg) == types.Message:
                        await error_occured(arg, e)
                        break
    return wrapper
