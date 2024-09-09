import logging
from aiogram import types
from datetime import datetime

from create_bot import bot
from .users import update_user, find_all_users
from ..connect import get_mongo_users, get_mongo_messages


async def create_user(message: types.Message):
    mongo_users = get_mongo_users()
    mongo_messages = get_mongo_messages()

    user_structure = {
        "_id": message.from_user.id,
        "info": {
            "time_registred": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "chat_id": message.chat.id,
            "email": "",
            "full_name": message.from_user.full_name,           # his name in tg
            "username": message.from_user.username,             # his tg tag
            "written_name": "",                                 # what was written in tg bot by user in /start
            "age": "",
            "program": {
                "name": "",
                "year": "",
            },
            "about": "",
        },
        "blacklist": [],                                        # of user_ids
        "blocked_bot": "no",
        "active_matching": "no",
        "finished_profile": "no",
        "cache": {},
    }

    messages_structure = {
        "_id": message.from_user.id,
        "messages": [],
    }

    await mongo_users.insert_one(user_structure)
    await mongo_messages.insert_one(messages_structure)

    logging.info(f"user_id '{message.from_user.id}' was added to MongoDB.")

    return


async def delete_everithing():
    mongo_users = get_mongo_users()
    mongo_messages = get_mongo_messages()

    await mongo_users.delete_many({})
    await mongo_messages.delete_many({})

    return


async def actualize_user(user_id: str):
    try:
        user: types.User = await bot.get_chat(user_id)
    except Exception as e:
        if "Forbidden" in str(e):
            await update_user(user_id, {"blocked_bot": "yes"})

        else:
            logging.exception(f"\nERROR: [Error retrieving chat for user {user_id}]\nTRACEBACK:")
        
        return


    await update_user(user_id, {
        "info.username": user.username,
        "info.full_name": user.full_name,
        }
    )

    return


async def actualize_all_users():
    users = await find_all_users(["_id", "blocked_bot", "active_matching"])

    for user in users:
        if user["blocked_bot"] == "no" and user["active_matching"] == "yes":
            await actualize_user(user["_id"])

    return
