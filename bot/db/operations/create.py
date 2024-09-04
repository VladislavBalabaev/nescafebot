import logging
from aiogram import types
from datetime import datetime

from .users import update_user, find_user
from ..connect import get_mongo_users, get_mongo_messages


async def create_user(user_id: str, chat_id: str, full_name: str, username: str):
    mongo_users = get_mongo_users()
    mongo_messages = get_mongo_messages()

    user_structure = {
        "_id": user_id,
        "info": {
            "time_registred": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "chat_id": chat_id,
            "email": "",
            "full_name": full_name,             # his name in tg
            "username": username,               # his tg tag
            "written_name": "",                 # what was written in tg bot by user in /start
            "age": "",
            "program": {
                "name": "",
                "year": "",
            },
            "about": "",
        },
        "blacklist": {
            "users": [],                        # of user_ids 
            "programs": []
        },
        "cache": {},
    }

    messages_structure = {
        "_id": user_id,
        "messages": [],
    }

    await mongo_users.insert_one(user_structure)
    await mongo_messages.insert_one(messages_structure)

    logging.info(f"user_id '{user_id}' was added to MongoDB.")

    return


async def delete_everithing():
    mongo_users = get_mongo_users()
    mongo_messages = get_mongo_messages()

    await mongo_users.delete_many({})
    await mongo_messages.delete_many({})

    return
