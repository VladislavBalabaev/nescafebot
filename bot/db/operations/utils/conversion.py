import re
import asyncio

from db.connect import get_mongo_users
from configs.selected_ids import ADMINS


username_id = {}
dict_lock = asyncio.Lock()


class UserConversion:
    def __init__(self) -> None:
        self.users_dict = {}
        self.dict_lock = asyncio.Lock()


    async def add(self, _id):
        mongo_users = get_mongo_users()

        username = await mongo_users.find_one({"_id": _id}, {"info.username": 1})
        username = username["info"]["username"]

        if _id in ADMINS:
            username += " \033[92m[admin]\033[0m"

        username_stripped = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]').sub('', username)
        username = f"({username + ')':<{25 + len(username) - len(username_stripped)}}"

        async with self.dict_lock:
            self.users_dict[_id] = username

        return username


    async def get(self, _id):
        async with self.dict_lock:
            username = self.users_dict.get(_id)

        if username is None:
            username = await self.add(_id)

        return username


user_conversion = UserConversion()
