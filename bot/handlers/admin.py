import logging
from aiogram import Dispatcher, types
from aiogram.filters.command import Command

from handlers import other
from configs.smth import ADMINS
from create_bot import dp, logs_path


@dp.message(Command("logs"))
async def cmd_send_logs(message: types.Message):
    if message.from_user.id in ADMINS:
        try:
            logging.info(f"Admin @{message.from_user.username} asked for logs.")

            await message.answer_document(types.FSInputFile(logs_path))
        except Exception as e:
            await other.error_occured(message, e)


def register_handlers_admin(dp: Dispatcher):
    dp.message.register(cmd_send_logs)
