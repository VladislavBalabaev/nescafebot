import asyncio

from handlers import client
from create_bot import dp, bot


client.register_handlers_client(dp)
# admin.register_handlers_admin(dp)


async def on_startup():
    print('### Bot started working! ###\n')
    # db.sql_start()


async def on_shutdown():
    print('\n### Bot has finished working! ###')


dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
