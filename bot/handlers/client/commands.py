import logging
# from aiogram.filters import Filter
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter

from handlers.utils.addressing_errors import error_sender


router = Router()


# class ContainTextFilter(Filter):
#     def __init__(self, text: str) -> None:
#         self.text = text

#     async def __call__(self, message: types.Message) -> bool:
#         return self.text in message.text
# THIS is bullshit: use F.text.lower().in_([])


@router.message(Command("cancel"))
@error_sender
async def cmd_cancel(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} canceled state {await state.get_state()}.")

    await state.clear()
    await message.answer("Все отменили!")


@router.message(StateFilter(None), Command("help"))
@error_sender
async def cmd_help(message: types.Message):
    raise NotImplementedError


# @router.message(StateFilter(None))   # catching all messages with "zero" condition (needs to be the last function)
# @error_sender
# async def zero_message(message: types.Message):
#     await message.answer(message.text)
