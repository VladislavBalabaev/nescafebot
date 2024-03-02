import asyncio
import logging
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from create_bot import dp
from handlers import other


class states_create_user(StatesGroup):
    name = State()
    age = State()
    faculty = State()
    about = State()
    city = State()


@dp.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    try:
        logging.info(f"User @{message.from_user.username} has started dialog.")

        await state.set_state(states_create_user.name)

        await message.answer("Привет!\nМы - там-то там-то, хотим то-то то-то.\nСейчас ты то-то то-то, давай начнем.")
        await asyncio.sleep(1)
        await message.answer("Введи свою фамилию и имя")
    except Exception as e:
        await other.error_occured(message, e)


@dp.message(StateFilter(states_create_user.name))
async def cu_process_name(message: types.Message, state: FSMContext):           # cu - create user
    try:
        logging.info(f"User @{message.from_user.username} wrote his name: {message.text}.")

        # await state.update_data(name=message.text) # REPLACE WITH REDIS

        await state.set_state(states_create_user.age)

        await message.answer("Сколько тебе лет?")
    except Exception as e:
        await other.error_occured(message, e)


@dp.message(StateFilter(states_create_user.age))
async def cu_process_age(message: types.Message, state: FSMContext):
    try:
        NotImplementedError
    except Exception as e:
        await other.error_occured(message, e)


@dp.message(StateFilter(states_create_user.faculty))
async def cu_process_faculty(message: types.Message, state: FSMContext):
    try:
        NotImplementedError
    except Exception as e:
        await other.error_occured(message, e)


@dp.message(StateFilter(states_create_user.about))
async def cu_process_about(message: types.Message, state: FSMContext):
    try:
        NotImplementedError
    except Exception as e:
        await other.error_occured(message, e)


@dp.message(StateFilter(states_create_user.city))
async def cu_process_city(message: types.Message, state: FSMContext):
    try:
        NotImplementedError
    except Exception as e:
        await other.error_occured(message, e)


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    NotImplementedError


@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    try:
        current_state = await state.get_state()
        if current_state is None:
            return

        logging.info(f"User @{message.from_user.username} canceled state {current_state}.")
        
        await state.clear()
        await message.answer("Все отменили!")
    except Exception as e:
        await other.error_occured(message, e)


@dp.message(StateFilter(None))   # catching all messages with "zero" condition (needs to be the last function)
async def zero_message(message: types.Message):
    try:
        await message.answer(message.text)
    except Exception as e:
        await other.error_occured(message, e)


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
