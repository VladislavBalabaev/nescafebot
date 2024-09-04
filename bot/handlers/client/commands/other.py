import logging
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from handlers.common.addressing_errors import error_sender


router = Router()


@router.message(Command("cancel"))
@error_sender
async def cmd_cancel(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} canceled state {await state.get_state()}.")

    await state.clear()
    await message.answer("Все отменили!")


@router.message(StateFilter(None), Command("help"))
@error_sender
async def cmd_help(message: types.Message, state: FSMContext):
    raise NotImplementedError


@router.message(StateFilter(None), Command("blacklist_show"))
@error_sender
async def cmd_see_blacklist(message: types.Message, state: FSMContext):
    raise NotImplementedError


# @router.message(StateFilter(None))   # catching all messages with "zero" condition (needs to be the last function)
# @error_sender
# async def zero_message(message: types.Message):
#     await message.answer(message.text)
