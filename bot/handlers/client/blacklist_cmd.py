import asyncio
import logging
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from handlers.common.addressing_errors import error_sender


router = Router()



class blacklist_states(StatesGroup):
    after_start_cmd = State()

    choose = State()

    block_person = State()
    after_block_person = State()

    block_faculty = State()
    after_block_faculty = State()


@router.message(StateFilter(blacklist_states.after_start_cmd))
@error_sender
async def notify_capabilities(message: types.Message, state: FSMContext):
    raise NotImplementedError


@router.message(StateFilter(None), Command("add_to_blacklist"))
@error_sender
async def cmd_blacklist(message: types.Message, state: FSMContext):
    raise NotImplementedError
    logging.info(f"User @{message.from_user.username} has started to write to his blacklist.")

    await state.set_state(blacklist_states.blacklist)

    await message.answer("Выбери, добавить в черный список faculty'year или конкретного человека?")
    # TODO: add opportunity to block whole facultie'year


@router.message(StateFilter(blacklist_states.choose))
@error_sender
async def blacklist_choose(message: types.Message, state: FSMContext):
    raise NotImplementedError


@router.message(StateFilter(blacklist_states.block_faculty))
@error_sender
async def blacklist_faculty(message: types.Message, state: FSMContext):
    raise NotImplementedError


@router.message(StateFilter(blacklist_states.after_block_faculty))
@error_sender
async def blacklist_choose(message: types.Message, state: FSMContext):
    raise NotImplementedError


@router.message(StateFilter(blacklist_states.block_person))
@error_sender
async def blacklist_person(message: types.Message, state: FSMContext):
    raise NotImplementedError
    person = message.text.strip().replace(' ', '').replace('@', '') # TODO: add different variants

    logging.info(f"User @{message.from_user.username} added @{person} to his blacklist.")

    # TODO: add written @tg to his REDIS blacklist

    await message.answer(f"@{person} был добавлен в твой черный список.")
    await message.answer(f"Хочешь продолжить?")


@router.message(StateFilter(blacklist_states.after_block_person))
@error_sender
async def blacklist_faculty(message: types.Message, state: FSMContext):
    raise NotImplementedError


