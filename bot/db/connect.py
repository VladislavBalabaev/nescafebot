import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from configs.env_reader import config


mongo_client = None
mongo_users = None


async def setup_mongo_connection():
    global mongo_client, mongo_users

    mongo_client = AsyncIOMotorClient(
        # f"mongodb://{config.MONGODB_USERNAME.get_secret_value()}:{config.MONGODB_PASSWORD.get_secret_value()}@mongo_DB:27017/?authMechanism=DEFAULT&directConnection=true"
        f"mongodb://{config.MONGODB_USERNAME.get_secret_value()}:{config.MONGODB_PASSWORD.get_secret_value()}@localhost:27017/?authMechanism=DEFAULT&directConnection=true"
    )

    databases = await mongo_client.list_database_names()

    mongo_users = mongo_client['userDatabase']['users']

    logging.info(f"MongoDB client has {databases} databases.")

    return


def get_mongo_users():
    global mongo_users

    if mongo_users is None:        
        raise Exception("MongoDB users collection not set up.")

    return mongo_users


def close_mongo_connection():
    global mongo_client

    mongo_client.close()

    return
