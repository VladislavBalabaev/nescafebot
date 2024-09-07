import os
import json
import logging
from aiogram import types, Router
from aiogram.filters import Filter
from aiogram.filters.state import StateFilter
from aiogram.filters.command import Command, CommandObject

from create_bot import bot
from configs.logs import logs_path
from configs.env_reader import TEMP_DIR
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


async def semd_temporary_file(user_id: str, text: str):
    file_path = TEMP_DIR / f"user_{user_id}.txt"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    await bot.send_document(user_id, document=types.FSInputFile(file_path))

    os.remove(file_path)

    return


@router.message(StateFilter(None), Command("admin"), AdminFilter())
@error_sender
async def cmd_admin(message: types.Message):
    logging.info(f"admin=@{message.from_user.username:<12} texted: {repr(message.text)}")

    await message.answer("/logs - текущие логи;\n/messages @tg 15 - последние N сообщений пользователя;\n/user @tg - данные пользователя;\n/match - сделать мэтчинг.")

    return


@router.message(StateFilter(None), Command("logs"), AdminFilter())
@error_sender
async def cmd_logs(message: types.Message,):
    logging.info(f"admin=@{message.from_user.username:<12} texted: {repr(message.text)}")

    await message.answer_document(types.FSInputFile(logs_path))

    return


@router.message(StateFilter(None), Command("messages"), AdminFilter())
@error_sender
async def cmd_messages(message: types.Message, command: CommandObject):
    logging.info(f"admin=@{message.from_user.username:<12} texted: {repr(message.text)}")

    if not command.args:
        await message.answer("Введи пользователя и кол-во сообщений:\n/messages @vbalab 30")
        return

    args = command.args.split()
    username = args[0].replace('@', '').replace(' ', '')
    n_messages = int(args[1])

    user_id = await find_id_by_username(username)

    messages = await find_messages(user_id)
    messages = messages[-n_messages:]
    messages_json = json.dumps(messages, indent=3, ensure_ascii=False)
    messages_formatted = f"<pre>{messages_json}</pre>"


    if len(messages_formatted) > 4000:
        await semd_temporary_file(user_id, messages_json)
    else:
        await message.answer(messages_formatted, parse_mode="HTML")

    return


@router.message(StateFilter(None), Command("user"), AdminFilter())
@error_sender
async def cmd_user(message: types.Message, command: CommandObject):
    logging.info(f"admin=@{message.from_user.username:<12} texted: {repr(message.text)}")

    if not command.args:
        await message.answer("Введи пользователя:\n/user @vbalab")

        return

    username = command.args.split()[0].replace('@', '').replace(" ", '')

    user_id = await find_id_by_username(username)
    user_info = await find_user(user_id)

    user_info = json.dumps(user_info, indent=3, ensure_ascii=False)

    await message.answer(f"<pre>{user_info}</pre>", parse_mode="HTML")

    return
