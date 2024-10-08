import logging
from datetime import datetime
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command, CommandObject

from handlers.common.checks import checker
from handlers.admin.matching import sending
from db.operations.messages import send_msg_user
from handlers.admin.admin_filter import AdminFilter
from handlers.admin.matching.assignment import match
from handlers.admin.matching.save import save_matching
from db.operations.user_profile import actualize_all_users
from db.operations.users import find_id_by_username, find_all_users


router = Router()


class SendMessageStates(StatesGroup):
    """
    State management for sending a message to a specific user.
    """
    MESSAGE = State()


class SendMessageToAllStates(StatesGroup):
    """
    State management for sending a message to all users.
    """
    MESSAGE = State()


@router.message(StateFilter(None), Command("match"), AdminFilter())
@checker
async def cmd_match(message: types.Message):
    """
    Executes the matching process, saving the results and notifying admins and users.
    """
    time_started = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    await actualize_all_users()
    logging.info(f"process='matching'                        !! Data of active users was actualized.")
 
    matched_df = await match()
    logging.info(f"process='matching'                        !! Users were matched; Emojis were attached.")

    await save_matching(matched_df, time_started)
    logging.info(f"process='matching'                        !! Results of matching were saved.")

    await sending.send_matching_admin(matched_df)
    logging.info(f"process='matching'                        !! Admins were notified.")

    await sending.send_matching_client(matched_df)
    logging.info(f"process='matching'                        !! Users were notified.")

    return


@router.message(StateFilter(None), Command("pseudo_match"), AdminFilter())
@checker
async def cmd_pseudo_match(message: types.Message):
    """
    Simulates the matching process and notifies admins of the results without saving them.
    """
    await actualize_all_users()
    logging.info(f"process='matching'                        !! Data of active users was actualized.")
 
    matched_df = await match()
    logging.info(f"process='matching'                        !! Users were matched; Emojis were attached.")

    await sending.send_matching_admin(matched_df)
    logging.info(f"process='matching'                        !! Admins were notified.")

    return


@router.message(StateFilter(None), Command("send_message"), AdminFilter())
@checker
async def cmd_send_message(message: types.Message, command: CommandObject, state: FSMContext):
    """
    Initiates the process to send a message to a specific user, prompting the admin for the message content.
    """
    if not command.args or len(command.args.split()) != 1:
        await send_msg_user(message.from_user.id, "Введи пользователя:\n/send_message @vbalab")
        return

    username = command.args.replace('@', '').replace(' ', '')

    user_id = await find_id_by_username(username)
    await state.update_data(user_id=user_id)

    await send_msg_user(message.from_user.id, "Введи сообщение")

    await state.set_state(SendMessageStates.MESSAGE)

    return


@router.message(StateFilter(SendMessageStates.MESSAGE), AdminFilter())
@checker
async def send_message_message(message: types.Message, state: FSMContext):
    """
    Sends the admin's message to the specified user and clears the state.
    """
    user_data = await state.get_data()
    user_id = user_data['user_id']

    await send_msg_user(user_id, message.text)

    await state.clear()

    return


@router.message(StateFilter(None), Command("send_message_to_all"), AdminFilter())
@checker
async def cmd_send_message_to_all(message: types.Message, state: FSMContext):
    """
    Initiates the process to send a message to all users, prompting the admin for the message content.
    """
    await send_msg_user(message.from_user.id, "Введи сообщение")

    await state.set_state(SendMessageToAllStates.MESSAGE)

    return


@router.message(StateFilter(SendMessageToAllStates.MESSAGE), AdminFilter())
@checker
async def send_message_to_all_message(message: types.Message, state: FSMContext):
    """
    Sends the admin's message to all users who have not blocked the bot and are active for matching.
    """
    users = await find_all_users(["_id", "info.username", "blocked_bot", "active_matching"])

    for user in users:
        if user["blocked_bot"] == "no" and user["active_matching"] == "yes":
            await send_msg_user(user["_id"], message.text)

    await state.clear()

    return
