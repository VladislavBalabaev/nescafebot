from enum import Enum
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from db.operations.users import find_user, update_user
from handlers.client.shared.check import check_profile
from handlers.common.addressing_errors import error_sender
from handlers.client.shared.keyboard import create_keyboard
from db.operations.messages import send_msg_user, recieve_msg_user


router = Router()


class ActiveStates(StatesGroup):
    ACTIVE = State()

    ACTIVATED = State()
    DEACTIVATED = State()


class ActiveYesNo(Enum):
    YES = "Да"
    NO = "Отмена"


@router.message(StateFilter(None), Command("active"))
@error_sender
@check_profile
async def cmd_active(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    active = await find_user(message.from_user.id, ["active_matching"])
    active = active["active_matching"]

    if active == "no":
        keyboard = create_keyboard(ActiveYesNo)
        await send_msg_user(message.from_user.id, 
                            "Твой аккаунт неактивен, а значит, ты не участвуешь в рандом кофе(\n\nХочешь сделать его обратно активным?", 
                            reply_markup=keyboard)

        await state.set_state(ActiveStates.ACTIVATED)
    else:
        keyboard = create_keyboard(ActiveYesNo)
        await send_msg_user(message.from_user.id, 
                            "Твой аккаунт активен, а значит, ты будешь участвовать в рандом кофе\n\n Хочешь отдохнуть от кофе и сделать его неактивным?", 
                            reply_markup=keyboard)

        await state.set_state(ActiveStates.DEACTIVATED)


@router.message(StateFilter(ActiveStates.ACTIVATED), F.text == ActiveYesNo.NO.value)
@router.message(StateFilter(ActiveStates.DEACTIVATED), F.text == ActiveYesNo.NO.value)
@error_sender
async def active_cancel(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await send_msg_user(message.from_user.id, 
                        "Окей)", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.clear()


@router.message(StateFilter(ActiveStates.ACTIVATED), F.text == ActiveYesNo.YES.value)
@error_sender
async def Active_after_block_person(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await update_user(message.from_user.id,
                      {"active_matching": "no"})

    await send_msg_user(message.from_user.id, 
                        "Теперь твой профиль неактивен\nПриходи, как будет желание)", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.clear()


@router.message(StateFilter(ActiveStates.DEACTIVATED), F.text == ActiveYesNo.YES.value)
@error_sender
async def Active_after_block_person(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await update_user(message.from_user.id,
                      {"active_matching": "yes"})

    await send_msg_user(message.from_user.id, 
                        "Теперь твой профиль активен!\nОсталось лишь дождаться следующего рандом кофе)", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.clear()
