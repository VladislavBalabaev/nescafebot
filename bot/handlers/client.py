import logging
from aiogram import Dispatcher, types
from aiogram.filters.command import Command

from create_bot import dp


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        logging.info(f"User @{message.from_user.username} started dialog.")

        await message.answer("Привет! Введи свое ФИО")
    except:
        logging.error(f"An error occured while starting dialog with user @{message.from_user.username}.")

        await message.answer("Извини, что-то пошло не так, мы получили ошибку, разберемся! Можешь написать ")


@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message):
    pass


@dp.message()   # catching all messages with "zero" condition (needs to be the last function)
async def zero_message(message: types.Message):
    try:
        await message.answer(message.text)
    except:
        pass


def register_handlers_client(dp: Dispatcher):
    dp.message.register(cmd_start)
    dp.message.register(cmd_cancel)
    dp.message.register(zero_message)
