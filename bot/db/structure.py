import json
import operator
from datetime import datetime
from functools import reduce

from db.connect import redis_users, redis_messages, pg_matching


user_structure = {
    "user_id": "",
    "chat_id": "",
    "info": {
        "full_name": "",            # his name in tg
        "username": "",             # his tg tag
        "name": "",                 # how he calls himself in bot
        "email": "",
        "age": "",
        "program": {
            "year": "",
            "name": "",
            },
        "about": "",
    },
    "messages": [],
    "blacklist": {
        "users": [],                # of user_ids 
        "programs": []
        },
}


def dict_get(data_dict, path):
    """Access a nested object in data_dict by item sequence."""
    return reduce(operator.getitem, path, data_dict)


def dict_set(data_dict, path, value):
    """Set a value in a nested object in data_dict by item sequence."""
    dict_get(data_dict, path[:-1])[path[-1]] = value


# def dict_del(data_dict, path):
#     """Delete a key-value in a nested object in data_dict by item sequence."""
#     del dict_get(data_dict, path[:-1])[path[-1]]


async def user_get(user_id, path = None):
    data = await redis_users.get(str(user_id))
    data = json.loads(data)

    if path:
        return dict_get(data, path)
    else:
        return data


async def user_set(user_id, path: list = None, value: str = None):
    if path:
        data = await redis_users.get(str(user_id))
        data = json.loads(data)

        dict_set(data, path, str(value))
    else:
        data = user_structure

    data = json.dumps(data)
    await redis_users.set(str(user_id), data)

    return


async def user_sent_msg(message, text: str = None):
    messages = await redis_users.get(str(message.from_user.id))
    messages = json.loads(messages)

    messages.append({
        "side": "bot",
        "datetime": datetime.now(),
        "message": text,
    })


    messages = json.dumps(messages)
    await user_set(str(message.from_user.id), ["messages"], messages)

    await message.answer(text)

    return


async def user_recieve_msg(message, text: str = None):
    messages = await redis_users.get(str(message.from_user.id))
    messages = json.loads(messages)

    messages.append({
        "side": "user",
        "datetime": datetime.now(),
        "message": text,
    })

    messages = json.dumps(messages)
    await user_set(str(message.from_user.id), ["messages"], messages)

    return


def save_redis_data():
    ...


def program_to_users(program: str = "MAE'25"):
    ...
