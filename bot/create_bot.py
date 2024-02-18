import os
# from redis import Redis
from aiogram import Bot, Dispatcher


bot = Bot(os.environ['NESCAFEBOT_TOKEN'])
# storage = Redis.Storage.from

# def get_store(redis_db: int) -> RedisStore:
#     settings = get_settings(

#     return RedisStore(
#         Redis(
#             host=settings.redis_host,
#             port=settings.redis_port,
#             decode_responses=True,
#             db=redis_db,
#         )
#     )


dp = Dispatcher()