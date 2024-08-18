import aioredis

from configs.env_reader import config

def connect_to_redis():
    redis_con = aioredis.from_url(
            url="redis://:" + config.REDIS_PASSWORD.get_secret_value() + "@redis_DB:6379", 
            decode_responses=True
        )

    return redis_con

redis_con = connect_to_redis()
