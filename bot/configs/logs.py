import asyncio
import logging
from queue import Queue
from logging import StreamHandler
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler

from .env_reader import bot_path


logs_path = bot_path / "data" / "logs" / "coffee.log"

logs_path.parent.mkdir(parents=True, exist_ok=True)


async def init_logger():
    que = Queue()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(QueueHandler(que))


    console_format = logging.Formatter("%(levelname)-8s :: %(asctime)s.%(msecs)03d :: %(message)s", "%H:%M:%S")
    console_handler = StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_format)


    file_format = logging.Formatter("%(levelname)-8s :: %(name)-20s :: %(asctime)s :: %(message)s :: (%(filename)s:%(lineno)d)")
    file_handler = RotatingFileHandler(logs_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_format)

    listener = QueueListener(que, console_handler, file_handler)

    try:
        listener.start()
        logging.debug(f'### Logger has been started! ###')

        while True:
            await asyncio.sleep(60)
    finally:
        logging.debug(f'### Logger is being shutdown! ###')
        listener.stop()
