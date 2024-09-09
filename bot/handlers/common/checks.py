from aiogram import types
from functools import wraps

from db.operations.messages import send_msg_user, recieve_msg_user


def text_checker(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        message = None

        for arg in args:
            if isinstance(arg, types.Message):
                message = arg

        message = kwargs.get("message", message)

        if message.text:
            await f(*args, **kwargs)
        else:
            await recieve_msg_user(message, fail=True)

            await send_msg_user(message.from_user.id, 
                                "Принимаем только текст)\nДавай заново",
                                fail=True)

    return wrapper
