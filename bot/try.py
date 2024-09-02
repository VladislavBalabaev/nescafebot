import asyncio
from db.connect import insert_user_data, get_user_data

async def main():
    user_id = "123456"
    name = "Alice"
    description = "A sample user"
    blacklist = ["spam", "ads"]
    whitelist = ["news", "technology"]

    await insert_user_data(user_id, name, description, blacklist, whitelist, "bot", "123", "asdasdjasdk")

    print(f'{user_id} was inserted into mongo_DB')

    user_data = await get_user_data(user_id)

    print(f"Retrieved user data: {user_id}")
    print(f"name: {user_data['name']}\n"
            f"description: {user_data['description']}\n"
            f"blacklist: {user_data['blacklist']}\n"
            f"whitelist: {user_data['whitelist']}\n"
            f"messages: {user_data['messages']}\n"
            f"messages->text: {user_data['messages']['text']}\n"
            )

if __name__ == "__main__":
    asyncio.run(main())