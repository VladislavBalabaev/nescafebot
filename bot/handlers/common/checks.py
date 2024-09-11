from aiogram import types
from functools import wraps

from db.operations.users import find_user
from .addressing_errors import error_sender
from db.operations.messages import send_msg_user, recieve_msg_user


async def has_finished_profile(message: types.Message) -> bool:
    finished_profile = await find_user(message.from_user.id, ["finished_profile"])
    finished_profile = finished_profile["finished_profile"]

    return finished_profile


def check_finished_profile(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        message = None
        for arg in args:
            if isinstance(arg, types.Message):
                message = arg
                break
        message = kwargs.get("message", message)


        finished_profile = await has_finished_profile(message)

        if finished_profile == "yes":
            await f(*args, **kwargs)
        else:
            await send_msg_user(message.from_user.id,
                          "У тебя еще нет аккаунта(\n\nПожалуйста, пройди регистрацию через /start")

    return wrapper


def text_checker(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        message = None
        for arg in args:
            if isinstance(arg, types.Message):
                message = arg
                break
        message = kwargs.get("message", message)


        if message.text:
            await f(*args, **kwargs)
        else:
            try:
                await send_msg_user(message.from_user.id, 
                                    "Принимаем только текст)\nДавай заново",
                                    fail=True)
            except TypeError:
                await send_msg_user(message.from_user.id, 
                                    "Чтобы зарегестрироваться в боте, напиши /start",
                                    fail=True)

    return wrapper


def receiver_msg(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        message = None
        for arg in args:
            if isinstance(arg, types.Message):
                message = arg
                break
        message = kwargs.get("message", message)

        await recieve_msg_user(message)
        await f(*args, **kwargs)

    return wrapper


def checker(f):
    return error_sender(receiver_msg(text_checker(f)))
