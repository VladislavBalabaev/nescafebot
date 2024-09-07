import logging
from datetime import datetime
from aiogram import types, Router
from aiogram.filters import Filter
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.state import StateFilter

from create_bot import bot
from configs.env_reader import BOT_DIR
from configs.selected_ids import ADMINS
from handlers.admin.matching.assignment import match
from handlers.admin.matching.sending import send_matching
from handlers.common.addressing_errors import error_sender
from db.operations.user_profile import actualize_all_users


MATCHING_DIR = BOT_DIR / "data" / "temporary"
MATCHING_DIR.mkdir(parents=True, exist_ok=True)


router = Router()


class AdminFilter(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in ADMINS


@router.message(StateFilter(None), Command("match"), AdminFilter())
@error_sender
async def cmd_match(message: types.Message):
    logging.info(f"admin=@{message.from_user.username:<12} texted: {repr(message.text)}")

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
@error_sender
async def cmd_send_message(message: types.Message, command: CommandObject):
    logging.info(f"admin=@{message.from_user.username:<12} texted: {repr(message.text)}")

    raise NotImplementedError
    return


@router.message(StateFilter(None), Command("send_message_to_all"), AdminFilter())
@error_sender
async def cmd_send_message_to_all(message: types.Message):
    logging.info(f"admin=@{message.from_user.username:<12} texted: {repr(message.text)}")

    raise NotImplementedError
    return
