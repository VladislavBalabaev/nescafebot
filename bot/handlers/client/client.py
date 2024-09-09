from aiogram import Dispatcher

from handlers.client import commands


def register_handlers_client(dp: Dispatcher):
    dp.include_routers(
        commands.cancel.router,                    # because /cancel is there
        commands.start.router,
        commands.blacklist.router,
        commands.active.router,
        commands.help_.router,
        commands.zero_message.router,
    )
