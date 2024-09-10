import logging
from aiogram import types
from datetime import datetime

from create_bot import bot
from db.connect import get_mongo_messages
from db.operations.user_profile import new_user, MongoDBUserNotFound


async def find_messages(user_id: int):
    mongo_messages = get_mongo_messages()

    messages = await mongo_messages.find_one({"_id": user_id}, {"messages": 1})
    try:
        messages = messages["messages"]
    except TypeError:
        raise MongoDBUserNotFound(f"User {user_id} is not found in MongoDB.")

    return messages


async def update_messages(user_id: int, messages):
    mongo_messages = get_mongo_messages()

    filter = {"_id": user_id}
    newvalues = { "$set": {"messages": messages}}

    await mongo_messages.update_one(filter, newvalues)

    return


async def delete_messages(user_id: int):
    mongo_messages = get_mongo_messages()
    
    await mongo_messages.delete_one({"_id": user_id})

    return


async def send_msg_user(user_id: int, text: str = None, fail: bool = False, reply_markup: types.ReplyKeyboardMarkup = None):
    logging.info(f"_id='{user_id:<10}' \033[36m<<\033[0m\033[91m{' [FAIL]' if fail else ''}\033[0m {repr(text)}")

    messages = await find_messages(user_id)

    messages.append({
        "side": "bot",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": text,
    })

    await update_messages(user_id, messages)

    await bot.send_message(user_id, text, reply_markup=reply_markup)

    return


@new_user
async def recieve_msg_user(message: types.Message, pending: bool = False, zero_message: bool = False):
    user_id = message.from_user.id

    messages = await find_messages(user_id)

    messages.append({
        "side": "user",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message.text,
    })

    await update_messages(user_id, messages)

    pending = " \033[91m[Pending]\033[0m" if pending else ''
    zero_message = " \033[91m[ZeroMessage]\033[0m" if zero_message else ''
    logging.info(f"_id='{user_id:<10}' \033[35m>>\033[0m{pending}{zero_message} {repr(message.text)}")

    return
