import asyncio

from configs import logs
from create_bot import dp, bot
from handlers.admin import admin
from handlers.client import client
from handlers.client.menu import set_commands
from handlers.admin.send_on import send_startup, send_shutdown
from handlers.common.pending import notify_users_with_pending_updates
from db.connect import setup_mongo_connection, close_mongo_connection


async def on_startup():
    _ = asyncio.create_task(logs.init_logger())
    await asyncio.sleep(0)

    await setup_mongo_connection()
    await send_startup()
    await notify_users_with_pending_updates()


async def on_shutdown():
    await send_shutdown()

    close_mongo_connection()


async def main():
    try:
        admin.register_handlers_admin(dp)
        client.register_handlers_client(dp)

        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        await set_commands(bot)

        await dp.start_polling(bot, drop_pending_updates=True)
    finally:
        pass


if __name__ == "__main__":
    asyncio.run(main())
