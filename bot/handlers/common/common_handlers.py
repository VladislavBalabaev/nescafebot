from aiogram import Dispatcher

from handlers.common import commands


def register_handler_cancel(dp: Dispatcher):
    dp.include_routers(
        commands.cancel.router,
    )


def register_handler_zero_message(dp: Dispatcher):
    dp.include_routers(
        commands.zero_message.router,
    )
