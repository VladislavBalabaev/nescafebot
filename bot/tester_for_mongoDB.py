import asyncio
import motor.motor_asyncio


from configs.env_reader import config

async def insert_user_data(user_id, name, description, blacklist, whitelist):
    user_data = {
        "_id": user_id,  # User ID as the key
        "name": name,
        "description": description,
        "blacklist": blacklist,
        "whitelist": whitelist
    }
    result = await users_collection.insert_one(user_data)

# Asynchronous function to get user data by ID
async def get_user_data(user_id):
    user = await users_collection.find_one({"_id": user_id})
    return user

async def main():
    user_id = "12345"
    name = "Alice"
    description = "A sample user"
    blacklist = ["spam", "ads"]
    whitelist = ["news", "technology"]
    await insert_user_data(user_id, name, description, blacklist, whitelist)
    print(f'{user_id} was inserted into mongo_DB')

    user_data = await get_user_data(user_id)
    print(f"Retrieved user data: {user_id}")
    print(f"name: {user_data['name']}\n"
          f"description: {user_data['description']}\n"
          f"blacklist: {user_data['blacklist']}\n"
          f"whitelist: {user_data['whitelist']}")


if __name__ == "__main__":
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://'+config.MONGODB_USERNAME.get_secret_value()+':'+config.MONGODB_PASSWORD.get_secret_value()+'@mongo_DB:27017/?authMechanism=DEFAULT&directConnection=true')
    db = client['userDatabase']
    users_collection = db['users']
    asyncio.run(main())
