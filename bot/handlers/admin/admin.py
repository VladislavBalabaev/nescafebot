from aiogram import Dispatcher

from handlers.admin.commands.all import router


def register_handlers_admin(dp: Dispatcher):
    dp.include_routers(router)
