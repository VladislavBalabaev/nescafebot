import logging
from aiogram.filters import Filter
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram import Dispatcher, types, Router

from configs.selected_ids import ADMINS
from create_bot import logs_path
from handlers.common.addressing_errors import error_sender


router = Router()


class AdminFilter(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in ADMINS


@router.message(StateFilter(None), Command("logs"), AdminFilter)
@error_sender
async def cmd_send_logs(message: types.Message):
    logging.info(f"Admin @{message.from_user.username} asked for logs.")

    await message.answer_document(types.FSInputFile(logs_path))


def register_handlers_admin(dp: Dispatcher):
    dp.include_routers(router)
