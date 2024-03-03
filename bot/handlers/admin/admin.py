import logging
from aiogram import Dispatcher, types, Router
from aiogram.filters.command import Command

from configs.smth import ADMINS
from create_bot import logs_path
from handlers.utils import error_sender


router = Router()


@router.message(Command("logs"))
@error_sender
async def cmd_send_logs(message: types.Message):
    if message.from_user.id in ADMINS:
        logging.info(f"Admin @{message.from_user.username} asked for logs.")

        await message.answer_document(types.FSInputFile(logs_path))\


def register_handlers_admin(dp: Dispatcher):
    dp.include_routers(router)
