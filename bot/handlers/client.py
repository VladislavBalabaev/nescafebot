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
        await message.answer("Извини, что-то пошло не так, мы получили ошибку, разберемся!")


@dp.message(Command(""))
async def cmd_reply(message: types.Message):
    await message.reply('Это ответ с "ответом"')


def register_handlers_client(dp: Dispatcher):
    dp.message.register(cmd_start)
