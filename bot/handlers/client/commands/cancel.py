from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from handlers.common.combined import checker
from db.operations.messages import send_msg_user, recieve_msg_user


router = Router()


@router.message(Command("cancel"))
@checker
async def cmd_cancel(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await send_msg_user(message.from_user.id, 
                        "Все отменили!", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.clear()

    return