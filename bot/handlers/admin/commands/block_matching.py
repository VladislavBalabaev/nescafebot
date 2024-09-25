import logging
from enum import Enum
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command

from handlers.common.checks import checker
from db.operations.messages import send_msg_user
from handlers.admin.admin_filter import AdminFilter
from handlers.client.shared.keyboard import create_keyboard
from handlers.client.shared.contains import contains_command
from db.operations.users import find_user, update_user, find_id_by_username


router = Router()


class BlockMatchingStates(StatesGroup):
    DECISION = State()

    BLOCK = State()
    AFTER_BLOCK = State()

    UNBLOCK = State()
    AFTER_UNBLOCK = State()


class BlockMatchingChoice(Enum):
    ADD = "Запретить мэтчинг"
    REMOVE = "Разрешить мэтчинг"
    CANCEL = "Отмена"


async def block_matching_add(username: str):
    user_id = find_id_by_username(username)

    has_blocked_matching = await find_user(user_id, ["blocked_matching"])
    has_blocked_matching = has_blocked_matching["blocked_matching"]

    if has_blocked_matching == "yes":
        return False

    await update_user(user_id, {"blocked_matching": "yes"})

    return True


async def block_matching_remove(username: str):
    user_id = find_id_by_username(username)

    has_blocked_matching = await find_user(user_id, ["blocked_matching"])
    has_blocked_matching = has_blocked_matching["blocked_matching"]

    if has_blocked_matching == "no":
        return False

    await update_user(user_id, {"blocked_matching": "no"})

    return True


@router.message(StateFilter(None), Command("block_matching"), AdminFilter())
@checker
async def cmd_block_matching(message: types.Message, state: FSMContext):
    keyboard = create_keyboard(BlockMatchingChoice)
    await send_msg_user(message.from_user.id, 
                        "Выбери, что будем делать:", 
                        reply_markup=keyboard)

    await state.set_state(BlockMatchingStates.DECISION)


@router.message(StateFilter(BlockMatchingStates.DECISION), F.text == BlockMatchingChoice.ADD.value)
@checker
@contains_command
async def block_matching_block(message: types.Message, state: FSMContext):
    await send_msg_user(message.from_user.id, 
                        "Напиши, кому запретить мэтчинг (напр., @person_tg)", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.set_state(BlockMatchingStates.BLOCK)


@router.message(StateFilter(BlockMatchingStates.BLOCK))
@checker
@contains_command
async def block_matching_after_block(message: types.Message, state: FSMContext):
    username = message.text.strip().replace(' ', '').replace('@', '')

    if await block_matching_add(username):
        logging.info(f"process='blocking matching'               !! User {username} has now matching blocked.")
        await send_msg_user(message.from_user.id,
                            f"Пользователь {username} теперь не будет участвовать в мэтчинге")
    else:
        await send_msg_user(message.from_user.id,
                            f"Этому пользователю мэтчинг уже был запрещен")

    await state.clear()


@router.message(StateFilter(BlockMatchingStates.DECISION), F.text == BlockMatchingChoice.REMOVE.value)
@checker
@contains_command
async def block_matching_unblock(message: types.Message, state: FSMContext):
    await send_msg_user(message.from_user.id, 
                        "Напиши, кого разрешить мэтчинг (напр., @person_tg)", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.set_state(BlockMatchingStates.UNBLOCK)


@router.message(StateFilter(BlockMatchingStates.UNBLOCK))
@checker
@contains_command
async def block_matching_after_unblock(message: types.Message, state: FSMContext):
    username = message.text.strip().replace(' ', '').replace('@', '')

    if await block_matching_remove(username):
        logging.info(f"process='blocking matching'               !! User {username} has now matching allowed.")
        await send_msg_user(message.from_user.id,
                            f"Пользователь {username} теперь будет участвовать в мэтчинге")
    else:
        await send_msg_user(message.from_user.id,
                            f"Этому пользователю мэтчинг уже был разрешен")

    await state.clear()


@router.message(StateFilter(BlockMatchingStates.DECISION), F.text == BlockMatchingChoice.CANCEL.value)
@checker
@contains_command
async def block_matching_end(message: types.Message, state: FSMContext):
    await send_msg_user(message.from_user.id,
                        "Хорошо",
                        reply_markup=types.ReplyKeyboardRemove())

    await state.clear()


def is_invalid_block_matching_choice(message: types.Message) -> bool:
    return message.text not in [choice.value for choice in BlockMatchingChoice]


@router.message(StateFilter(BlockMatchingStates.DECISION), is_invalid_block_matching_choice)
@checker
@contains_command
async def block_matching_no_command_choice(message: types.Message):
    keyboard = create_keyboard(BlockMatchingChoice)
    await send_msg_user(message.from_user.id, 
                        "Выбери из предложенных вариантов", 
                        reply_markup=keyboard)

    return
