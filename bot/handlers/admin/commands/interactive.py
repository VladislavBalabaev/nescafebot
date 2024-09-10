import logging
from datetime import datetime
from aiogram import types, Router
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command, CommandObject

from create_bot import bot
from configs.env_reader import BOT_DIR
from configs.selected_ids import ADMINS
from handlers.common.checks import checker
from db.operations.messages import send_msg_user
from handlers.admin.matching.assignment import match
from handlers.admin.matching.sending import send_matching
from db.operations.user_profile import actualize_all_users
from db.operations.users import find_id_by_username, find_all_users



MATCHING_DIR = BOT_DIR / "data" / "temporary"
MATCHING_DIR.mkdir(parents=True, exist_ok=True)


router = Router()


class SendMessageStates(StatesGroup):
    MESSAGE = State()


class SendMessageToAllStates(StatesGroup):
    MESSAGE = State()


class AdminFilter(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in ADMINS


@router.message(StateFilter(None), Command("match"), AdminFilter())
@checker
async def cmd_match(message: types.Message):
    await actualize_all_users()
    logging.info(f"MATCHING: Data of all users was actualized.")

    matched_df = await match()
    logging.info(f"MATCHING: Users were matched; Emojis were attached.")

    file_path = MATCHING_DIR / f"matched_data_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.xlsx"
    matched_df.to_excel(file_path, index=True)
    logging.info(f"MATCHING: Results of matching were saved.")

    await bot.send_document(message.from_user.id, document=types.FSInputFile(file_path))
    logging.info(f"MATCHING: Admin was notified.")

    await send_matching(matched_df)
    logging.info(f"MATCHING: Users were notified.")

    return


@router.message(StateFilter(None), Command("send_message"), AdminFilter())
@checker
async def cmd_send_message(message: types.Message, command: CommandObject, state: FSMContext):
    if not command.args or len(command.args.split()) != 1:
        await message.answer("Введи пользователя:\n/send_message @vbalab")
        return

    username = command.args.replace('@', '').replace(' ', '')

    user_id = await find_id_by_username(username)
    await state.update_data(user_id=user_id)

    await message.answer("Введи сообщение")

    await state.set_state(SendMessageStates.MESSAGE)

    return



@router.message(StateFilter(SendMessageStates.MESSAGE), AdminFilter())
@checker
async def send_message_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data['user_id']

    await send_msg_user(user_id, message.text)

    await state.clear()

    return


@router.message(StateFilter(None), Command("send_message_to_all"), AdminFilter())
@checker
async def cmd_send_message_to_all(message: types.Message, state: FSMContext):
    await message.answer("Введи сообщение")

    await state.set_state(SendMessageToAllStates.MESSAGE)

    return


@router.message(StateFilter(SendMessageToAllStates.MESSAGE), AdminFilter())
@checker
async def send_message_to_all_message(message: types.Message, state: FSMContext):
    users = await find_all_users(["_id", "info.username", "blocked_bot", "active_matching"])

    for user in users:
        if user["blocked_bot"] == "no" and user["active_matching"] == "yes":
            await send_msg_user(user["_id"], message.text)

    await state.clear()

    return
