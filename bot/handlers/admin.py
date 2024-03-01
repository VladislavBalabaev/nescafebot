import logging
from pathlib import Path
from aiogram import Dispatcher, types
from aiogram import filters
from aiogram.filters.command import Command

from create_bot import dp
from configs.smth import ADMINS


path = Path("logs")
logs_path = path / "coffee.log"


@dp.message(Command("logs"))
async def cmd_send_logs(message: types.Message):
    if message.from_user.id in ADMINS:
        try:
            logging.info(f"User @{message.from_user.username} asked for logs.")
            
            await message.answer_document(types.FSInputFile(logs_path))
        except:
            logging.error(f"An error occured while user @{message.from_user.username} asked for logs.")

            await message.answer("Что-то не так.")


def register_handlers_admin(dp: Dispatcher):
    dp.message.register(cmd_send_logs)
