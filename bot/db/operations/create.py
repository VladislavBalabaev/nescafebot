import logging
from aiogram import types

from .users import update_user, find_user
from ..connect import get_mongo_users, get_mongo_messages


async def create_user(user_id: str, chat_id: str, full_name: str, username: str):
    mongo_users = get_mongo_users()
    mongo_messages = get_mongo_messages()

    user_structure = {
        "_id": user_id,
        "info": {
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


async def create_or_update_on_start(message: types.Message):
    user_id = message.from_user.id

    data = await find_user(user_id, ["_id"])

    if data:
        to_update = {
            "info.chat_id": str(message.chat.id),
            "info.full_name": str(message.from_user.full_name),
            "info.username": str(message.from_user.username),
        }

        await update_user(user_id, to_update)
    else:
        await create_user(
            user_id=user_id,
            chat_id=message.chat.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            )

    return


async def delete_everithing():
    mongo_users = get_mongo_users()
    mongo_messages = get_mongo_messages()

    await mongo_users.delete_many({})
    await mongo_messages.delete_many({})

    return
