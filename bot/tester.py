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
    print("Print arg1 arg2 arg3")
    args = input().split(" ")
    await redis_con.hset("hash", mapping={"key1": args[0], "key2": args[1], "key3": args[2]})
    result = await redis_con.hgetall("hash")
    print(result)

    await redis_con.close()


if __name__ == "__main__":
    asyncio.run(main())

    


