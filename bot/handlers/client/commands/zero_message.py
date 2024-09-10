import logging
from datetime import datetime
from aiogram import types, Router
from aiogram.filters.state import StateFilter

from handlers.common.checks import checker
from db.operations.messages import send_msg_user, update_messages, find_messages


router = Router()


@router.message(StateFilter(None))   # catching all messages with "zero" condition (needs to be the last function)
@checker
async def zero_message(message: types.Message):
    user_id = message.from_user.id

    logging.info(f"_id='{user_id}'        texted \033[91m[ZeroMessage]\033[0m: {repr(message.text)}")

    messages = await find_messages(user_id)

    messages.append({
        "side": "user",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message.text,
    })

    await update_messages(user_id, messages)

    await send_msg_user(user_id, 
                        "Выбери что-нибудь из Menu")

    return