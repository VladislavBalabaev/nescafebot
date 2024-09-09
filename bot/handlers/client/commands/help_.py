from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from handlers.common.addressing_errors import error_sender
from db.operations.messages import send_msg_user, recieve_msg_user


router = Router()


@router.message(StateFilter(None), Command("help"))
@error_sender
async def cmd_help(message: types.Message):
    await recieve_msg_user(message)

    await send_msg_user(message.from_user.id, 
                        "Ты можешь открыть Menu, там находятся все доступные тебе команды)\n\nЕсли хочешь создать (если еще не создан) или обновить профиль, напиши /start.\nПосмотреть черный список, добавить в него или исключить из, выбери /blacklist.\nПосмотреть будет ли аккаунт участвовать в следующем кофе - /active.\n\nЕсли еще остались вопросы, не стесняйся, пиши @vbalab и/или @Madfyre, обязательно тебе поможем)")

    return