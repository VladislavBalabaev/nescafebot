from aiogram import types, Router
from aiogram.filters.state import StateFilter

from handlers.common.addressing_errors import error_sender
from db.operations.messages import send_msg_user, recieve_msg_user


router = Router()


@router.message(StateFilter(None))   # catching all messages with "zero" condition (needs to be the last function)
@error_sender
async def zero_message(message: types.Message):
    await recieve_msg_user(message, zero_message=True)

    await send_msg_user(message.from_user.id, 
                        "Выбери что-нибудь из Menu")

    return