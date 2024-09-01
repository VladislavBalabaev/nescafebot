import asyncio
import logging
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from handlers.common.addressing_errors import error_sender
from db.structure import user_get, user_set, user_recieve_msg, user_sent_msg


router = Router()


class start_states(StatesGroup):
    name = State()
    age = State()
    program = State()
    about = State()
    city = State()


@router.message(StateFilter(None), Command("start"))
@error_sender
async def cmd_start(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} has started dialog.")

    await user_set(message.from_user.id)
    await user_set(message.from_user.id, ["user_id"], message.from_user.id)
    await user_set(message.from_user.id, ["chat_id"], message.chat.id)
    await user_set(message.from_user.id, ["info", "full_name"], message.from_user.full_name)
    await user_set(message.from_user.id, ["info", "username"], message.from_user.username)

    user_sent_msg(message,
                   "Привет!\nМы - там-то там-то, хотим то-то то-то.\nСейчас ты то-то то-то, давай начнем.")

    await asyncio.sleep(1)

    user_sent_msg(message.from_user.id, "Как тебя зовут?")

    await state.set_state(start_states.name)


    data = await user_get(message.from_user.id)
    print(data)


@router.message(StateFilter(start_states.name))
@error_sender
async def start_name(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} wrote his name: {message.text}.")

    # TODO: await state.update_data(name=message.text) # REPLACE WITH REDIS

    await state.set_state(start_states.age)

    await message.answer("Сколько тебе лет?")


@router.message(StateFilter(start_states.age))
@error_sender
async def start_age(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} wrote his age: {message.text}.")

    if message.text.isdigit():
        # TODO: await state.update_data(name=int(message.text)) # REPLACE WITH REDIS

        await state.set_state(start_states.program)

        await message.answer("Напиши свою программу в формате\n\"программа год_окончания\" (e.g. MAE 2025)")
    else:
        await message.answer("Это было не число)\nДавай заново")        


@router.message(StateFilter(start_states.program))
@error_sender
async def start_program(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} wrote his program: {message.text}.")

    # TODO: await state.update_data(name=int(message.text)) # REPLACE WITH REDIS

    await state.set_state(start_states.about)

    await message.answer("Напиши о себе, своих интересах")



@router.message(StateFilter(start_states.about))
@error_sender
async def start_about(message: types.Message, state: FSMContext):
    raise NotImplementedError


@router.message(StateFilter(start_states.city))
@error_sender
async def start_city(message: types.Message, state: FSMContext):
    raise NotImplementedError
