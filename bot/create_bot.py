import os
from pathlib import Path
from aiogram import Bot, Dispatcher

from configs.env_reader import config


logs_path = Path("logs") / "coffee.log"


bot = Bot(config.NESCAFEBOT_TOKEN.get_secret_value())
dp = Dispatcher()
