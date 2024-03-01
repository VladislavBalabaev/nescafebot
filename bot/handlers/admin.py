import logging
from pathlib import Path
from aiogram import Dispatcher, types
from aiogram.filters.command import Command

from create_bot import bot, dp
from handlers import other
from configs.smth import ADMINS


path = Path("logs")
logs = types.FSInputFile(Path("logs") / "coffee.log")


@dp.message(Command("logs"))
async def cmd_send_logs(message: types.Message):
    if message.from_user.id in ADMINS:
        try:
            logging.info(f"User @{message.from_user.username} asked for logs.")

            await message.answer_document(logs)
        except:
            logging.error(f"An error occured while user @{message.from_user.username} asked for logs.")

            await other.send_error_message(message)


async def send_logs():
    for admin in ADMINS:
        await bot.send_message(admin, "Bot has finished working!")
        await bot.send_document(admin, document=logs)


def register_handlers_admin(dp: Dispatcher):
    dp.message.register(cmd_send_logs)
