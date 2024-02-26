import asyncio
import logging

from configs import logs
from handlers import client
from create_bot import dp, bot


client.register_handlers_client(dp)
# admin.register_handlers_admin(dp)


async def on_startup():
    _ = asyncio.create_task(logs.init_logger())
    await asyncio.sleep(0)

    logging.info("### Bot has started working! ###\n")
    
    # db.sql_start()


async def on_shutdown():
    logging.info("\n### Bot has finished working! ###")


dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        pass


if __name__ == "__main__":
    asyncio.run(main())
