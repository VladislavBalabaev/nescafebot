import asyncio
from motor import motor_asyncio

from configs.env_reader import config




def get_users_db():
    client = motor_asyncio.AsyncIOMotorClient(
        # f"mongodb://{config.MONGODB_USERNAME.get_secret_value()}:{config.MONGODB_PASSWORD.get_secret_value()}@mongo_DB:27017/?authMechanism=DEFAULT&directConnection=true"
        f"mongodb://{config.MONGODB_USERNAME.get_secret_value()}:{config.MONGODB_PASSWORD.get_secret_value()}@localhost:27017/?authMechanism=DEFAULT&directConnection=true"
        )

    db = client['userDatabase']
    users = db['users']

    return users


mongo_users = get_users_db()


async def insert_user_data(user_id, name, description, blacklist, whitelist, side, time, text):
    global mongo_users

    user_data = {
        "_id": user_id,  # User ID as the key
        "name": name,
        "description": description,
        "blacklist": blacklist,
        "whitelist": whitelist,
        "messages": {
            "side": side,
            "time": time,
            "text": text
        }
    }
    await mongo_users.insert_one(user_data)


async def get_user_data(user_id):
    global mongo_users

    user = await mongo_users.find_one({"_id": user_id})
    return user
