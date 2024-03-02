import asyncio
import logging

from configs import logs
from create_bot import dp, bot
from handlers import admin, client, other


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)


async def on_startup():
    _ = asyncio.create_task(logs.init_logger())
    await asyncio.sleep(0)

    logging.info("### Bot has started working! ###")
    
    # db.sql_start()


async def on_shutdown():
    logging.info("### Bot has finished working! ###")

    await other.send_logs()

dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)


async def main():
    try:
        # await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        pass


if __name__ == "__main__":
    asyncio.run(main())
