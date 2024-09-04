import asyncio
from random import randint
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from ..email import send_email
from db.operations.users import update_user, find_user
from db.operations.create import create_or_update_on_start
from handlers.common.addressing_errors import error_sender
from db.operations.messages import send_msg_user, recieve_msg_user


router = Router()


class start_states(StatesGroup):
    email_get = State()
    email_set = State()
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
                        "Какая у тебя @nes.ru почта?\n\nОна нужна нам, чтобы мы могли подтвердить, что ты студент РЭШ")

    await state.set_state(start_states.email_get)


@router.message(StateFilter(start_states.email_get))
@error_sender
async def cmd_start(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    if "@nes.ru" in message.text:
        await send_msg_user(message.from_user.id, 
                            "Секундочку")

        code = str(randint(100000, 999999))

        await update_user(message.from_user.id,
                        {"cache.email": message.text, "cache.email_code": code})

        await send_email(message.text, f"Привет!\nТвой код для NEScafeBot: {code}.\nКод был отправлен для аккаунта @{message.from_user.username}")

        await send_msg_user(message.from_user.id, 
                            "Мы отправили тебе на почту код из 6 цифр.\nНапиши его, пожалуйста, сюда")

        await state.set_state(start_states.email_set)
    else:
        await send_msg_user(message.from_user.id, 
                            "Это не почта РЭШ\nДавай заново",
                            fail=True)


@router.message(StateFilter(start_states.email_set))
@error_sender
async def cmd_start(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    cache = await find_user(message.from_user.id, ["cache"])
    email_code = cache["cache"]["email_code"]

    if message.text.replace(' ', '') == email_code:
        email = cache["cache"]["email"]

        await update_user(message.from_user.id, 
                          {"info.email": email, "cache": {}})

        await send_msg_user(message.from_user.id, 
                            "Отлично!\nПривязали почту к твоему аккаунту")

        await send_msg_user(message.from_user.id, 
                            "Как тебя зовут?")

        await state.set_state(start_states.name)
    else:
        await send_msg_user(message.from_user.id, 
                            "Код неверный)\nДавай заново",
                            fail=True)


@router.message(StateFilter(start_states.name))
@error_sender
async def start_name(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    if len(message.text) < 50:
        await update_user(message.from_user.id, 
                          {"info.written_name": message.text})

        await send_msg_user(message.from_user.id, 
                            "Сколько тебе лет?")

        await state.set_state(start_states.age)
    else:
        await send_msg_user(message.from_user.id, 
                            "Слишком длинное имя)\nДавай заново",
                            fail=True)


@router.message(StateFilter(start_states.age))
@error_sender
async def start_age(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    if message.text.isdigit():
        await update_user(message.from_user.id, 
                          {"info.age": message.text})

        await send_msg_user(message.from_user.id, 
                            "Напиши свою программу в формате\n\"'программа_год окончания'\" (e.g. MAE_2025)")

        await state.set_state(start_states.program)
    else:
        await send_msg_user(message.from_user.id, 
                            "Это было не число)\nДавай заново",
                            fail=True)


@router.message(StateFilter(start_states.program))
@error_sender
async def start_program(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    if '_' in message.text:
        program = message.text.split('_')
        await update_user(message.from_user.id, 
                        {"info.program.name": program[0], "info.program.year": program[1]})

        await send_msg_user(message.from_user.id, 
                            "Напиши о себе в паре предложений")

        await state.set_state(start_states.about)
    else:
        await send_msg_user(message.from_user.id, 
                            "Напиши именно в нужном формате)\nКак, например, MAE_2025",
                            fail=True)


@router.message(StateFilter(start_states.about))
@error_sender
async def start_about(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await update_user(message.from_user.id, 
                    {"info.about": message.text})

    await send_msg_user(message.from_user.id, 
                        "Пока падажжи, ебана, делаем еще.")

    await state.clear()
