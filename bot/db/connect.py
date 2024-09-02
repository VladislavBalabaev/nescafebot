from motor import motor_asyncio

from configs.env_reader import config


def get_users_db():
    client = motor_asyncio.AsyncIOMotorClient(
        # f"mongodb://{config.MONGODB_USERNAME.get_secret_value()}:{config.MONGODB_PASSWORD.get_secret_value()}@mongo_DB:27017/?authMechanism=DEFAULT&directConnection=true"
        f"mongodb://{config.MONGODB_USERNAME.get_secret_value()}:{config.MONGODB_PASSWORD.get_secret_value()}@localhost:27017/?authMechanism=DEFAULT&directConnection=true"
        )

    return client['userDatabase']['users']


mongo_users = get_users_db()
