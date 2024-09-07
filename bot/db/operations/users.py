import logging

from ..connect import get_mongo_users


async def update_user(user_id: str, keys_values: dict):
    mongo_users = get_mongo_users()

    filter = {"_id": user_id}
    newvalues = { "$set": keys_values}

    await mongo_users.update_one(filter, newvalues)

    logging.info(f"_id='{user_id}' {list(newvalues['$set'].keys())} were updated in DB.")

    return


async def find_user(user_id: str, keys: list = []):
    mongo_users = get_mongo_users()

    keys = {k: 1 for k in keys}

    if keys:
        user = await mongo_users.find_one({"_id": user_id}, keys)
    else:
        user = await mongo_users.find_one({"_id": user_id})

    return user


async def find_all_users(keys: list = []):
    mongo_users = get_mongo_users()

    keys = {k: 1 for k in keys}

    if keys:
        users_cursor = mongo_users.find({}, keys)
    else:
        users_cursor = mongo_users.find()

    users = await users_cursor.to_list(length=None)

    return users


async def delete_user(user_id: str):
    mongo_users = get_mongo_users()
    
    await mongo_users.delete_one({"_id": user_id})

    return


async def find_id_by_username(username: str):
    mongo_users = get_mongo_users()

    user = await mongo_users.find_one({"info.username": username}, 
                                      {"_id": 1, "info.username": 1})

    return user["_id"]


async def blacklist_add(user_id: str, username):
    blacklist = await find_user(user_id, ["blacklist"])
    blacklist = blacklist["blacklist"]

    if username in blacklist:
        return False

    blacklist.append(username)

    await update_user(user_id, {"blacklist": blacklist})

    return True


async def blacklist_remove(user_id: str, username):
    blacklist = await find_user(user_id, ["blacklist"])
    blacklist = blacklist["blacklist"]

    try:
        blacklist.remove(username)        
    except Exception:
        return False

    await update_user(user_id, {"blacklist": blacklist})

    return True
