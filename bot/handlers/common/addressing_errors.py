import logging
from aiogram import types
from functools import wraps
from aiogram.fsm.context import FSMContext

from create_bot import bot
from configs.selected_ids import ADMINS


async def error_occured(message: types.Message, state: FSMContext, error: Exception):
    logging.exception("The traceback of the ERROR:")

    await message.answer("Извини, что-то пошло не так(\nМы уже получили ошибку, разберемся!\n\nЕсли долго не чиним, можешь написать @Madfyre и/или @vbalab по поводу бота.")

    for admin in ADMINS:
        await bot.send_message(admin, f"Error, check the logs.\nUser: @{message.from_user.username}.\nState: {await state.get_state()}.\nMessage: \"{message.text}\".\n----------\n\n{error.__class__.__name__ }: {error}")


def error_sender(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            await f(*args, **kwargs)

        except Exception as e:
            if "message" in kwargs.keys():
                message = kwargs["message"]
            else:
                for arg in args:
                    if type(arg) == types.Message:
                        message = arg
                        break
            
            if "state" in kwargs.keys():
                state = kwargs["state"]
            else:
                for arg in args:
                    if type(arg) == FSMContext:
                        state = arg
                        break

            await error_occured(message=message, state=state, error=e)
    return wrapper
