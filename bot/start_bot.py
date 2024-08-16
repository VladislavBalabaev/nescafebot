import asyncio
import logging

from configs import logs
from create_bot import dp, bot
from handlers.admin import admin
from handlers.client import client
from redis_connection import connect_to_redis
from handlers.common.menu import set_commands
from handlers.admin.send import send_startup, send_shutdown


async def on_startup():
    await connect_to_redis()
    _ = asyncio.create_task(logs.init_logger())
    await asyncio.sleep(0)

    logging.info("### Bot has started working! ###")

    await send_startup()

    # db.sql_start()


async def on_shutdown():
    logging.info("### Bot has finished working! ###")

    await send_shutdown()


async def main():
    try:
        client.register_handlers_client(dp)
        admin.register_handlers_admin(dp)

        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        await set_commands(bot)

        # await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        pass


if __name__ == "__main__":
    asyncio.run(main())
