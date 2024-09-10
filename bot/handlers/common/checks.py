import logging
from aiogram import types
from functools import wraps

from db.operations.users import find_user
from .addressing_errors import error_sender
from db.operations.messages import send_msg_user, recieve_msg_user


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
            try:
                await recieve_msg_user(message, fail=True)

                await send_msg_user(message.from_user.id, 
                                    "Принимаем только текст)\nДавай заново",
                                    fail=True)
            except TypeError:
                await send_msg_user(message.from_user.id, 
                                    "Чтобы зарегестрироваться в боте, напиши /start",
                                    fail=True)

    return wrapper


def checker(f):
    return error_sender(text_checker(f))
