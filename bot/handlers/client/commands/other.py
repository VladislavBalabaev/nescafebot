from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from handlers.common.addressing_errors import error_sender
from db.operations.messages import send_msg_user, recieve_msg_user


router = Router()


@router.message(Command("cancel"))
@error_sender
async def cmd_cancel(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await send_msg_user(message.from_user.id, 
                        "Все отменили!", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.clear()


@router.message(StateFilter(None), Command("help"))
@error_sender
async def cmd_help(message: types.Message, state: FSMContext):
    raise NotImplementedError


# @router.message(StateFilter(None))   # catching all messages with "zero" condition (needs to be the last function)
# @error_sender
# async def zero_message(message: types.Message):
#     await message.answer(message.text)
