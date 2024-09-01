from aiogram import Bot, Dispatcher
from configs.env_reader import config


bot = Bot(token=config.NESCAFEBOT_TOKEN.get_secret_value())

dp = Dispatcher()
