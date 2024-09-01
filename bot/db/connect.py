import aioredis

from configs.env_reader import config


def connect_to_redis_users():
    redis_con = aioredis.from_url(
            url="redis://:" + config.REDIS_PASSWORD.get_secret_value() + "@redis_DB:6379", 
            decode_responses=True,
            db=1,
        )

    return redis_con


def connect_to_redis_messages():
    redis_con = aioredis.from_url(
            url="redis://:" + config.REDIS_PASSWORD.get_secret_value() + "@redis_DB:6379", 
            decode_responses=True,
            db=2,
        )

    return redis_con


def connect_to_pg_matching():
    # TODO: create postgre db for matching
    pg_con = ...

    return pg_con


redis_users = connect_to_redis_users()
redis_messages = connect_to_redis_messages()
pg_matching = connect_to_pg_matching()
