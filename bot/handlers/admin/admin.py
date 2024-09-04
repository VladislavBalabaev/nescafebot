import json
import logging
from aiogram.filters import Filter
from aiogram.filters.state import StateFilter
from aiogram import Dispatcher, types, Router
from aiogram.filters.command import Command, CommandObject

from create_bot import bot
from configs.logs import logs_path
from configs.selected_ids import ADMINS
from db.operations.messages import find_messages
from handlers.common.addressing_errors import error_sender
from db.operations.users import find_user, find_id_by_username


router = Router()


class AdminFilter(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in ADMINS


@router.message(StateFilter(None), Command("admin"), AdminFilter())
@error_sender
async def cmd_admin(message: types.Message):
    logging.info(f"admin=@{message.from_user.username:<12} texted: {repr(message.text)}")

    await message.answer("/logs - чтобы посмотреть текущие логи;\n/get_messages @tg 15 - чтобы посмотреть последние N сообщений пользователя;\n/get_user @tg - получить данные пользователя.")

    return


@router.message(StateFilter(None), Command("logs"), AdminFilter())
@error_sender
async def cmd_send_logs(message: types.Message,):
    logging.info(f"admin=@{message.from_user.username:<12} texted: {repr(message.text)}")

    await message.answer_document(types.FSInputFile(logs_path))

    return


@router.message(StateFilter(None), Command("get_messages"), AdminFilter())
@error_sender
async def cmd_get_messages(message: types.Message, command: CommandObject):
    """Like: /see_messages vbalab 20"""
    logging.info(f"admin=@{message.from_user.username:<12} texted: {repr(message.text)}")

    if not command.args:
        await message.answer("Введи пользователя и кол-во сообщений:\n/get_messages @vbalab 30")

        return

    args = command.args.split()
    username = args[0].replace('@', '').replace(' ', '')
    n_messages = int(args[1])

    user_id = await find_id_by_username(username)
    messages = await find_messages(user_id)
    messages = messages[-n_messages:]

    messages = json.dumps(messages, indent=3, ensure_ascii=False)

    await message.answer(f"<pre>{messages}</pre>", parse_mode="HTML")

    return


@router.message(StateFilter(None), Command("get_user"), AdminFilter())
@error_sender
async def cmd_get_user(message: types.Message, command: CommandObject):
    logging.info(f"admin=@{message.from_user.username:<12} texted: {repr(message.text)}")

    if not command.args:
        await message.answer("Введи пользователя:\n/get_user @vbalab")

        return

    username = command.args.split()[0].replace('@', '').replace(" ", '')

    user_id = await find_id_by_username(username)
    user_info = await find_user(user_id)

    user_info = json.dumps(user_info, indent=3, ensure_ascii=False)

    await message.answer(f"<pre>{user_info}</pre>", parse_mode="HTML")

    return


def register_handlers_admin(dp: Dispatcher):
    dp.include_routers(router)
