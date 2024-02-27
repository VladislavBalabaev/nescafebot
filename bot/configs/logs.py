from pathlib import Path
import asyncio
import logging
from queue import Queue
from logging import StreamHandler
from logging.handlers import QueueHandler, QueueListener


path = Path('logs')

path.mkdir(parents=True, exist_ok=True)


logging.basicConfig(
    filename=path / "coffee.log",
    encoding="utf-8",
    # format="",
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def init_logger():
    logger = logging.getLogger()            # to not use root logger
    # this logger has no handlers and it will propagate all events to be handled by root logger
    # best: make one logger per major-subcomponent of all project
    # debug -> info -> warning -> error -> critical
    
    que = Queue()
    
    logger.addHandler(QueueHandler(que))
    logger.setLevel(logging.DEBUG)
    
    listener = QueueListener(que, StreamHandler())
    try:
        logging.debug(f'Logger is being started.')
        listener.start()
        logging.debug(f'Logger has been started started.')
        
        while True:
            await asyncio.sleep(60)
    finally:
        logging.debug(f'Logger is shutting down.')
        listener.stop()