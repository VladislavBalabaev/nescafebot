import os
from pathlib import Path
from aiogram import Bot, Dispatcher


logs_path = Path("logs") / "coffee.log"


bot = Bot(os.environ['NESCAFEBOT_TOKEN'])

dp = Dispatcher()
