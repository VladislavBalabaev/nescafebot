import logging
from aiogram import types
from datetime import datetime

from create_bot import bot
from ..connect import get_mongo_messages


async def find_messages(user_id: str):
    mongo_messages = get_mongo_messages()

    messages = await mongo_messages.find_one({"_id": user_id}, {"messages": 1})
    messages = messages["messages"]

    return messages


async def update_messages(user_id: str, messages):
    mongo_messages = get_mongo_messages()

    filter = {"_id": user_id}
    newvalues = { "$set": {"messages": messages}}

    await mongo_messages.update_one(filter, newvalues)

    return


async def delete_messages(user_id: str):
    mongo_messages = get_mongo_messages()
    
    await mongo_messages.delete_one({"_id": user_id})

    return


async def send_msg_user(user_id: str, text: str = None):
    logging.info(f"user_id '{user_id}' received text: {repr(text)}")

    messages = await find_messages(user_id)

    messages.append({
        "side": "bot",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": text,
    })

    await update_messages(user_id, messages)

    await bot.send_message(user_id, text)

    return


async def recieve_msg_user(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"user_id '{user_id}'        texted: {repr(message.text)}")

    messages = await find_messages(user_id)

    messages.append({
        "side": "user",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message.text,
    })

    await update_messages(user_id, messages)

    return
