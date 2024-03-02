import asyncio
import logging
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from create_bot import dp
from handlers.utils import error_sender


class states_create_user(StatesGroup):
    name = State()
    age = State()
    faculty = State()
    about = State()
    city = State()


@dp.message(StateFilter(None), Command("start"))
@error_sender
async def cmd_start(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} has started dialog.")

    await state.set_state(states_create_user.name)

    await message.answer("Привет!\nМы - там-то там-то, хотим то-то то-то.\nСейчас ты то-то то-то, давай начнем.")
    await asyncio.sleep(1)
    await message.answer("Введи свою фамилию и имя")


@dp.message(StateFilter(states_create_user.name))
@error_sender
async def cu_process_name(message: types.Message, state: FSMContext):           # cu - create user
    logging.info(f"User @{message.from_user.username} wrote his name: {message.text}.")

    # await state.update_data(name=message.text) # REPLACE WITH REDIS

    await state.set_state(states_create_user.age)

    await message.answer("Сколько тебе лет?")


@dp.message(StateFilter(states_create_user.age))
@error_sender
async def cu_process_age(message: types.Message, state: FSMContext):
    raise NotImplementedError


@dp.message(StateFilter(states_create_user.faculty))
@error_sender
async def cu_process_faculty(message: types.Message, state: FSMContext):
    raise NotImplementedError


@dp.message(StateFilter(states_create_user.about))
@error_sender
async def cu_process_about(message: types.Message, state: FSMContext):
    raise NotImplementedError


@dp.message(StateFilter(states_create_user.city))
@error_sender
async def cu_process_city(message: types.Message, state: FSMContext):
    raise NotImplementedError


@dp.message(Command("help"))
@error_sender
async def cmd_help(message: types.Message):
    raise NotImplementedError


@dp.message(Command("cancel"))
@error_sender
async def cmd_cancel(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} canceled state {await state.get_state()}.")
    
    await state.clear()
    await message.answer("Все отменили!")


@dp.message(StateFilter(None))   # catching all messages with "zero" condition (needs to be the last function)
@error_sender
async def zero_message(message: types.Message):
    await message.answer(message.text)


def register_handlers_client(dp: Dispatcher):
    dp.message.register(cmd_start)
    dp.message.register(cu_process_name)
    dp.message.register(cu_process_age)
    dp.message.register(cu_process_faculty)
    dp.message.register(cu_process_about)
    dp.message.register(cu_process_city)
    dp.message.register(cmd_help)
    dp.message.register(cmd_cancel)
    dp.message.register(zero_message)
