import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from start_bot import dp, bot


@dp.message(Command("/start"))
async def cmd_answer(message: types.Message):
    try:
        await message.answer("Привет! Введи свое ФИО")
    except:
        await message.answer("Извини, что-то пошло не так, мы получили ошибку, разберемся!")        # TODO: check wether to use .answer of .reply


@dp.message(Command(""))
async def cmd_reply(message: types.Message):
    await message.reply('Это ответ с "ответом"')