import asyncio
import logging

from configs import logs
from create_bot import dp, bot
from handlers.admin import admin
from handlers.client import client
from handlers.common.menu import set_commands
from handlers.admin.send import send_startup, send_shutdown
from db.connect import connect_to_redis_users, connect_to_redis_messages


async def on_startup():
    _ = asyncio.create_task(logs.init_logger())
    await asyncio.sleep(0)

    logging.info("### Bot has started working! ###")

    await send_startup()


async def on_shutdown():
    await send_shutdown()
    logging.info("### Bot has finished working! ###")

    await connect_to_redis_users.close()
    await connect_to_redis_messages.close()
    logging.info("### Redis has finished working! ###")


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
