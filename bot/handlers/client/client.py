from aiogram import Dispatcher

from handlers import client


def register_handlers_client(dp: Dispatcher):
    dp.include_routers(
        client.commands.router,
        client.start_cmd.router,
        client.blacklist_cmd.router,
    )
