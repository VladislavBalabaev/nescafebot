import os
from aiogram import Bot, Dispatcher


bot = Bot(os.environ['NESCAFEBOT_TOKEN'])

dp = Dispatcher()