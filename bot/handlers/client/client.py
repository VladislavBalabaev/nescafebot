from aiogram import Dispatcher

from handlers import client


def register_handlers_client(dp: Dispatcher):
    dp.include_routers(
        client.start.router,
        client.blacklist.router,
        client.other.router,
    )
