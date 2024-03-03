from aiogram import Dispatcher

from handlers.client import commands, start_cmd


def register_handlers_client(dp: Dispatcher):
    dp.include_routers(
        commands.router,
        start_cmd.router,
    )
