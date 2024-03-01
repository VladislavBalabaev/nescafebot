import logging
from aiogram import Dispatcher, types
from aiogram.filters.command import Command

from create_bot import dp
from handlers import other



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        logging.info(f"User @{message.from_user.username} started dialog.")

        await message.answer("Привет! Введи свое ФИО")
    except:
        await other.error_occured(message)


@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message):
    pass


@dp.message()   # catching all messages with "zero" condition (needs to be the last function)
async def zero_message(message: types.Message):
    await message.answer(message.text)


def register_handlers_client(dp: Dispatcher):
    dp.message.register(cmd_start)
    dp.message.register(cmd_cancel)
    dp.message.register(zero_message)
