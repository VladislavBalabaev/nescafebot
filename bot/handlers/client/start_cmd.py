import asyncio
import logging
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from db.operations.users import update_user
from db.operations.create import create_or_update_on_start
from handlers.common.addressing_errors import error_sender
from db.operations.messages import send_msg_user, recieve_msg_user


router = Router()


class start_states(StatesGroup):
    name = State()
    age = State()
    program = State()
    about = State()

 
@router.message(StateFilter(None), Command("start"))
@error_sender
async def cmd_start(message: types.Message, state: FSMContext):
    # await delete_everithing()
    await create_or_update_on_start(message)

    await recieve_msg_user(message)

    await send_msg_user(message.from_user.id, 
                        "Привет!\nМы - там-то там-то, хотим то-то то-то.\nСейчас ты то-то то-то, давай начнем.")

    await asyncio.sleep(1)
    await send_msg_user(message.from_user.id, 
                        "Как тебя зовут?")

    await state.set_state(start_states.name)


@router.message(StateFilter(start_states.name))
@error_sender
async def start_name(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    if len(message.text) < 50:
        await update_user(message.from_user.id, 
                          {"info": {"written_name": message.text}})

        await send_msg_user(message.from_user.id, 
                            "Сколько тебе лет?")

        await state.set_state(start_states.age)
    else:
        await send_msg_user(message.from_user.id, 
                            "Слишком длинное имя)\nДавай заново")


@router.message(StateFilter(start_states.age))
@error_sender
async def start_age(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    if message.text.isdigit():
        await update_user(message.from_user.id, 
                          {"info": {"age": message.text}})

        await send_msg_user(message.from_user.id, 
                            "Напиши свою программу в формате\n\"'программа_год окончания'\" (e.g. MAE_2025)")

        await state.set_state(start_states.program)
    else:
        await send_msg_user(message.from_user.id, 
                            "Это было не число)\nДавай заново")


@router.message(StateFilter(start_states.program))
@error_sender
async def start_program(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    if '_' in message.text:
        program = message.text.split('_')
        await update_user(message.from_user.id, 
                        {"info": {"program": {"name": program[0], "year": program[1]}}})

        await send_msg_user(message.from_user.id, 
                            "Напиши о себе в паре предложений")

        await state.set_state(start_states.about)
    else:
        await send_msg_user(message.from_user.id, 
                            "Напиши именно в нужном формате)\nКак, например, MAE_2025")


@router.message(StateFilter(start_states.about))
@error_sender
async def start_about(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await update_user(message.from_user.id, 
                    {"info": {"about": message.text}})

    await send_msg_user(message.from_user.id, 
                        "Пока падажжи, ебана, делаем еще.")

    await state.clear()
