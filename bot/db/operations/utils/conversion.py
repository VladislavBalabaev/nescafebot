import asyncio

from configs.selected_ids import ADMINS
from db.operations.users import find_user


username_id = {}
dict_lock = asyncio.Lock()

class UserConversion:
    def __init__(self) -> None:
        self.users_dict = {}
        self.dict_lock = asyncio.Lock()


    async def add(self, _id):
        username = await find_user(_id, ["info.username"])
        username = username["info"]["username"]

        if _id in ADMINS:
            username += " \033[92m[admin]\033[0m"

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
