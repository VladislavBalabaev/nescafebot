import logging
from aiogram import types, exceptions

from create_bot import bot
from configs.logs import logs_path
from configs.selected_ids import ADMINS


async def send_startup():
    """
    Sends a startup notification to all admins and logs the startup event.
    """
    logging.info("### Bot has started working! ###")

    for admin in ADMINS:
        try:
            await bot.send_message(admin, "Bot has started working!")
        except exceptions.TelegramBadRequest as e:
            logging.error(f"Failed to send startup message to {admin}")


async def send_shutdown():
    """
    Sends a shutdown notification and the bot's logs to all admins, and logs the shutdown event.
    """
    logging.info("### Bot has finished working! ###")

    for admin in ADMINS:
        try:
            await bot.send_document(admin, document=types.FSInputFile(logs_path), caption="Bot has finished working!")
        except exceptions.TelegramBadRequest as e:
            logging.error(f"Failed to send startup message to {admin}")
