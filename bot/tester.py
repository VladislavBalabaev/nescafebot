import asyncio
import logging
import aioredis

from configs.env_reader import config

redis_con = None

async def connect_to_redis():
    global redis_con
    if redis_con is None:
        redis_con = await aioredis.from_url("redis://:" + config.REDIS_PASSWORD.get_secret_value() + "@redis_DB:6379")

async def main():
    await connect_to_redis()
    await redis_con.hset("hash", mapping={"key1": "value1", "key2": "value2", "key3": 123})
    result = await redis_con.hgetall("hash")
    print(result)

    await redis_con.close()


if __name__ == "__main__":
    asyncio.run(main())

    


