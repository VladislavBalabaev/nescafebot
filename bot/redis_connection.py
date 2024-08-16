import logging
import asyncio
import aioredis

redis_con = None

async def connect_to_redis():
    logging.info("### Trying to connect to Redis DB! ###")
    print("### Trying to connect to Redis DB! ###")
    # global redis_con
    if redis_con is None:
        redis_con = await aioredis.from_url("redis://redis_DB:6379", decode_responses=True)
        logging.info("### DB was connected! ###")
    


