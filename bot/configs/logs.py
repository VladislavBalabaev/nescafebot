import asyncio
import logging
from queue import Queue
from pathlib import Path
from logging import StreamHandler
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler


path = Path('logs')
logs_path = path / "coffee.log"

console_format = logging.Formatter("%(asctime)s.%(msecs)03d :: %(message)s", "%H:%M:%S")
file_format = logging.Formatter("%(levelname)-8s :: %(name)-20s :: %(asctime)s :: %(message)s :: (%(filename)s:%(lineno)d)")


async def init_logger():
    path.mkdir(parents=True, exist_ok=True)

    que = Queue()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(QueueHandler(que))

    console_handler = StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_format)

    file_handler = RotatingFileHandler(logs_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_format)

    listener = QueueListener(que, console_handler, file_handler)

    try:
        logging.debug(f'Logger is being started.')
        listener.start()
        logging.debug(f'Logger has been started.')

        while True:
            await asyncio.sleep(60)
    finally:
        logging.debug(f'Logger is being shutdown.')
        listener.stop()
