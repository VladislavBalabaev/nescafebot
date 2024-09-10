from enum import Enum
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from handlers.client.shared.keyboard import create_keyboard
from handlers.common.checks import checker, check_finished_profile
from db.operations.messages import send_msg_user, recieve_msg_user
from db.operations.users import blacklist_add, blacklist_remove, find_user


router = Router()


class BlacklistStates(StatesGroup):
    BLACKLIST = State()

    BLOCK_PERSON = State()
    AFTER_BLOCK_PERSON = State()

    UNBLOCK_PERSON = State()
    AFTER_UNBLOCK_PERSON = State()


class BlacklistChoice(Enum):
    ADD = "Добавлять в ЧС"
    REMOVE = "Удалять из ЧС"
    CANCEL = "Отмена"


class BlacklistYesNo(Enum):
    YES = "Да"
    NO = "Нет"


@router.message(StateFilter(None), Command("blacklist"))
@checker
@check_finished_profile
async def cmd_blacklist(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await send_msg_user(message.from_user.id, 
                        "Люди из черного списка не будут предлагаться тебе и ты не будешь предложен(а) им на последующих кофе.\n\nСейчас ты можешь добавить какого-либо конкретного человека через его @tg, а также удалить человека из черного списка, если он там находится.")

    blacklist = await find_user(message.from_user.id, ["blacklist"])
    blacklist = blacklist["blacklist"]
    if blacklist:
        blacklist = '\n'.join([f"@{user}" for user in blacklist])
        await send_msg_user(message.from_user.id,
                            f"У тебя есть пользователи в чс:\n{blacklist}")
    else:
        await send_msg_user(message.from_user.id,
                            "Пока что твой черный список пуст")

    keyboard = create_keyboard(BlacklistChoice)
    await send_msg_user(message.from_user.id, 
                        "Выбери, что будем делать:", 
                        reply_markup=keyboard)

    await state.set_state(BlacklistStates.BLACKLIST)


@router.message(StateFilter(BlacklistStates.BLACKLIST), F.text == BlacklistChoice.ADD.value)
@router.message(StateFilter(BlacklistStates.AFTER_BLOCK_PERSON), F.text == BlacklistYesNo.YES.value)
@checker
async def blacklist_block_person(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await send_msg_user(message.from_user.id, 
                        "Напиши, кого добавить в чс (напр., @person_tg)", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.set_state(BlacklistStates.BLOCK_PERSON)


@router.message(StateFilter(BlacklistStates.BLOCK_PERSON))
@checker
async def blacklist_after_block_person(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    username = message.text.strip().replace(' ', '').replace('@', '')

    if await blacklist_add(message.from_user.id, username):
        await send_msg_user(message.from_user.id,
                            f"Добавили в твой черный список.\nНа последующих кофе @{username} тебе не попадется!")
    else:
        await send_msg_user(message.from_user.id,
                            f"Этот пользователь уже есть в твоем черном списке")

    keyboard = create_keyboard(BlacklistYesNo)
    await message.answer(
        f"Хочешь добавить @tg ещё кого-нибудь?", 
        reply_markup=keyboard
        )

    await state.set_state(BlacklistStates.AFTER_BLOCK_PERSON)


@router.message(StateFilter(BlacklistStates.BLACKLIST), F.text == BlacklistChoice.REMOVE.value)
@router.message(StateFilter(BlacklistStates.AFTER_UNBLOCK_PERSON), F.text == BlacklistYesNo.YES.value)
@checker
async def blacklist_unblock_person(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await send_msg_user(message.from_user.id, 
                        "Напиши, кого исключить из чс (напр., @person_tg)", 
                        reply_markup=types.ReplyKeyboardRemove())

    await state.set_state(BlacklistStates.UNBLOCK_PERSON)


@router.message(StateFilter(BlacklistStates.UNBLOCK_PERSON))
@checker
async def blacklist_after_unblock_person(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    username = message.text.strip().replace(' ', '').replace('@', '')

    if await blacklist_remove(message.from_user.id, username):
        await send_msg_user(message.from_user.id,
                            f"Исключили из твоего черного списка!")
    else:
        await send_msg_user(message.from_user.id,
                            f"Этого пользователя не было в твоем черном списке")

    keyboard = create_keyboard(BlacklistYesNo)
    await send_msg_user(message.from_user.id,
                        f"Хочешь исключить из ЧС ещё чей-нибудь @tg?", 
                        reply_markup=keyboard)

    await state.set_state(BlacklistStates.AFTER_UNBLOCK_PERSON)


@router.message(StateFilter(BlacklistStates.BLACKLIST), F.text == BlacklistChoice.CANCEL.value)
@router.message(StateFilter(BlacklistStates.AFTER_BLOCK_PERSON), F.text == BlacklistYesNo.NO.value)
@router.message(StateFilter(BlacklistStates.AFTER_UNBLOCK_PERSON), F.text == BlacklistYesNo.NO.value)
@checker
async def blacklist_end(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await send_msg_user(message.from_user.id,
                        "Хорошо",
                        reply_markup=types.ReplyKeyboardRemove())

    blacklist = await find_user(message.from_user.id, ["blacklist"])
    blacklist = blacklist["blacklist"]

    if blacklist:
        blacklist = '\n'.join([f"@{user}" for user in blacklist])
        await send_msg_user(message.from_user.id,
                            f"Твои люди в чс:\n{blacklist}")
    else:
        await send_msg_user(message.from_user.id,
                            "Твой черный список пуст")

    await state.clear()
