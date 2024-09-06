from aiogram import Dispatcher

from handlers.client import commands


def register_handlers_client(dp: Dispatcher):
    dp.include_routers(
        commands.other.router,                    # because /cancel is there
        commands.start.router,
        commands.blacklist.router,
    )
