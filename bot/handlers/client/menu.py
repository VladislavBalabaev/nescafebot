from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="/start",
            description="Создать свой профиль"
        ),
        BotCommand(
            command="/cancel",
            description="Отменить текущий диалог"
        ),
        BotCommand(
            command="/active",
            description="Активен ли аккаунт"
        ),
        BotCommand(
            command="/blacklist",
            description="Черный список"
        ),
        BotCommand(
            command="/help",
            description="О чем этот бот"
        ),
    ]

    await bot.set_my_commands(commands)
