import os
from aiogram import Bot
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

# from database import db
from handlers import client, admin


token = os.environ['NESCAFEBOT_TOKEN']

bot = Bot(token)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Bot started working')
    # db.sql_start()

async def on_shutdown(_):
    print('Bot has finished working')



client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
# other.register_handler_other(dp)


executor.start_polling(
    dp,
    skip_updates=True,               # skip_updates=True for skipping updates when Bot is offline
    on_startup=on_startup,
    on_shutdown=on_shutdown
    )

