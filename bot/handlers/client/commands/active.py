from enum import Enum
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from db.operations.messages import send_msg_user
from db.operations.users import find_user, update_user
from handlers.client.shared.keyboard import create_keyboard
from handlers.client.shared.contains import contains_command
from handlers.common.checks import checker, check_finished_profile


router = Router()


class ActiveStates(StatesGroup):
    """
    State management for checking if a user's account is active or inactive.
    """
    ACTIVE = State()
    ACTIVATED = State()
    DEACTIVATED = State()


class ActiveChoice(Enum):
    """
    Enum for user choices to activate or deactivate their account.
    """
    YES = "Да"
    NO = "Не менять"


@router.message(StateFilter(None), Command("active"))
@checker
@check_finished_profile
async def cmd_active(message: types.Message, state: FSMContext):
    """
    Handles the /active command to check if a user wants to activate or deactivate their account.
    Prompts the user for their choice and sets the appropriate state.
    """
    active = await find_user(message.from_user.id, ["active_matching"])
    active = active["active_matching"]

    if active == "no":
        keyboard = create_keyboard(ActiveChoice)
        await send_msg_user(message.from_user.id, 
                            "Твой аккаунт неактивен, а значит, ты не участвуешь в рандом кофе(\n\nХочешь сделать его обратно активным?", 
                            reply_markup=keyboard)

        await state.set_state(ActiveStates.DEACTIVATED)
    else:
        keyboard = create_keyboard(ActiveChoice)
        await send_msg_user(message.from_user.id, 
                            "Твой аккаунт активен, а значит, ты будешь участвовать в рандом кофе\n\nХочешь отдохнуть от кофе и сделать его неактивным?", 
                            reply_markup=keyboard)

        await state.set_state(ActiveStates.ACTIVATED)


@router.message(StateFilter(ActiveStates.ACTIVATED), F.text == ActiveChoice.NO.value)
@router.message(StateFilter(ActiveStates.DEACTIVATED), F.text == ActiveChoice.NO.value)
@checker
@contains_command
async def active_cancel(message: types.Message, state: FSMContext):
    """
    Cancels the activation/deactivation process if the user selects "No."
    """
    await send_msg_user(message.from_user.id, 
                        "Хорошо", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.clear()


@router.message(StateFilter(ActiveStates.ACTIVATED), F.text == ActiveChoice.YES.value)
@checker
@contains_command
async def Active_after_block_person(message: types.Message, state: FSMContext):
    """
    Deactivates the user's account when they confirm by choosing "Yes."
    """
    await update_user(message.from_user.id,
                      {"active_matching": "no"})

    await send_msg_user(message.from_user.id, 
                        "Теперь твой профиль неактивен\nПриходи, как будет желание)", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.clear()


@router.message(StateFilter(ActiveStates.DEACTIVATED), F.text == ActiveChoice.YES.value)
@checker
@contains_command
async def Active_after_block_person(message: types.Message, state: FSMContext):
    """
    Activates the user's account when they confirm by choosing "Yes."
    """
    await update_user(message.from_user.id,
                      {"active_matching": "yes"})

    await send_msg_user(message.from_user.id, 
                        "Теперь твой профиль активен!\nОсталось лишь дождаться следующего рандом кофе)", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.clear()


def is_invalid_active_choice(message: types.Message) -> bool:
    """
    Checks if the user input is a valid choice for activating or deactivating their account.
    """
    return message.text not in [choice.value for choice in ActiveChoice]


@router.message(StateFilter(ActiveStates.ACTIVATED, ActiveStates.DEACTIVATED), is_invalid_active_choice)
@checker
@contains_command
async def blacklist_no_command(message: types.Message):
    """
    Informs the user to select from the available options if an invalid choice is made.
    """
    keyboard = create_keyboard(ActiveChoice)
    await send_msg_user(message.from_user.id, 
                        "Выбери из предложенных вариантов", 
                        reply_markup=keyboard)

    return
