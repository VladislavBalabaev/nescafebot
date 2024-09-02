import logging
from aiogram import types
from datetime import datetime

from create_bot import bot
from .connect import get_mongo_users


async def create_user(user_id: str, chat_id: str, full_name: str, username: str):
    mongo_users = get_mongo_users()

    user_structure = {
        "_id": user_id,
        "chat_id": chat_id,
        "info": {
            "full_name": full_name,             # his name in tg
            "username": username,               # his tg tag
            "email": "",
            "age": "",
            "program": {
                "year": "",
                "name": "",
                },
            "about": "",
        },
        "blacklist": {
            "users": [],                        # of user_ids 
            "programs": []
            },
        "messages": [],
    }

    await mongo_users.insert_one(user_structure)

    logging.info(f"user_id '{user_id}' -:- was added to DB.")

    return


async def update_user(user_id: str, keys_values: dict):
    mongo_users = get_mongo_users()

    filter = {"_id": user_id}
    newvalues = { "$set": keys_values}

    await mongo_users.update_one(filter, newvalues)

    logging.info(f"user_id '{user_id}' -:- values for {list(newvalues.keys())} were updated in DB.")

    return


async def find_user(user_id: str, keys: list = []):
    mongo_users = get_mongo_users()

    keys = {k: 1 for k in keys}

    if keys:
        user = await mongo_users.find_one({"_id": user_id}, keys)
    else:
        user = await mongo_users.find_one({"_id": user_id})

    return user


async def delete_user(user_id: str):
    mongo_users = get_mongo_users()
    
    await mongo_users.delete_one({"_id": user_id})

    return


async def delete_all_users():
    mongo_users = get_mongo_users()
    
    await mongo_users.delete_many({})

    return


async def send_msg_user(user_id: str, text: str = None):
    messages = await find_user(user_id, ["messages"])
    messages = messages["messages"]

    messages.append({
        "side": "bot",
        "datetime": str(datetime.now()),
        "message": text,
    })

    await update_user(user_id, {"messages": messages})

    await bot.send_message(user_id, text,)

    return


async def recieve_msg_user(message: types.Message):
    user_id = message.from_user.id

    messages = await find_user(user_id, ["messages"])
    messages = messages["messages"]

    messages.append({
        "side": "user",
        "datetime": str(datetime.now()),
        "message": message.text,
    })

    await update_user(user_id, {"messages": messages})

    return


def program_to_users(program: str = "MAE'25"):
    ...
