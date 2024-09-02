import asyncio
import logging
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from handlers.common.addressing_errors import error_sender
from db.structure import create_user, update_user, find_user, send_msg_user, recieve_msg_user, delete_all_users


router = Router()


class start_states(StatesGroup):
    name = State()
    age = State()
    program = State()
    about = State()
    city = State()


async def create_or_update_on_start(message: types.Message):
    user_id = message.from_user.id

    data = await find_user(user_id, ["_id"])

    if data:
        to_update = {
        "chat_id": str(message.chat.id),
        "info": {
            "full_name": str(message.from_user.full_name),
            "username": str(message.from_user.username),
            }
        }

        await update_user(user_id, to_update)
    else:
        await create_user(
            user_id=user_id,
            chat_id=message.chat.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            )

    return

 
@router.message(StateFilter(None), Command("start"))
@error_sender
async def cmd_start(message: types.Message, state: FSMContext):
    logging.info(f"user_id '{message.from_user.id}' -:- typed /start.")

    await delete_all_users()
    await create_or_update_on_start(message)

    await send_msg_user(message.from_user.id, "Привет!\nМы - там-то там-то, хотим то-то то-то.\nСейчас ты то-то то-то, давай начнем.")

    await asyncio.sleep(1)
    await send_msg_user(message.from_user.id, "Как тебя зовут?")

    await state.set_state(start_states.name)


    data = await find_user(message.from_user.id)
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
