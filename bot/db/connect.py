import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from configs.env_reader import config


mongo_client = None
mongo_users = None
mongo_messages = None


async def setup_mongo_connection():
    global mongo_client, mongo_users, mongo_messages

    mongo_client = AsyncIOMotorClient(
        # f"mongodb://{config.MONGODB_USERNAME.get_secret_value()}:{config.MONGODB_PASSWORD.get_secret_value()}@mongo_DB:27017/?authMechanism=DEFAULT&directConnection=true"
        f"mongodb://{config.MONGODB_USERNAME.get_secret_value()}:{config.MONGODB_PASSWORD.get_secret_value()}@localhost:27017/?authMechanism=DEFAULT&directConnection=true"
    )


    databases = await mongo_client.list_database_names()
    if "userDatabase" not in databases:
        raise Exception("'userDatabase' is NOT in 'mongoDB'")

    mongo_users = mongo_client['userDatabase']['users']
    mongo_messages = mongo_client['userDatabase']['messages']

    logging.info("### MongoDB has started working! ###")

    return


def get_mongo_users():
    global mongo_users

    if mongo_users is None:        
        raise Exception("MongoDB 'users' collection not set up.")

    return mongo_users


def get_mongo_messages():
    global mongo_messages

    if mongo_messages is None:        
        raise Exception("MongoDB 'messages' collection not set up.")

    return mongo_messages


def close_mongo_connection():
    global mongo_client

    mongo_client.close()

    logging.info("### MongoDB has finished working! ###")

    return
