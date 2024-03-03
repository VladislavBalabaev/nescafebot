from aiogram import Dispatcher

from handlers.client import additional, start


def register_handlers_client(dp: Dispatcher):
    dp.include_routers(
        start.router,
        additional.router,
    )
