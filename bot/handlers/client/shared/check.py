import logging
from aiogram import types
from functools import wraps

from db.operations.users import find_user
from db.operations.messages import send_msg_user


async def has_finished_profile(message: types.Message) -> bool:
    finished_profile = await find_user(message.from_user.id, ["finished_profile"])
    finished_profile = bool(finished_profile["finished_profile"])

    return finished_profile


def check_profile(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        if "message" in kwargs.keys():
            message = kwargs["message"]
        else:
            for arg in args:
                if type(arg) == types.Message:
                    message = arg
                    break


        finished_profile = await has_finished_profile(message)

        if finished_profile:
            await f(*args, **kwargs)
        else:
            logging.info(f"_id='{message.from_user.id}'    no profile: \033[91m[{message.text}]\033[0m.")
            send_msg_user(message.from_user.id,
                          "У тебя еще нет аккаунта(\n\nПожалуйста, пройди регистрацию через /start")

    return wrapper
