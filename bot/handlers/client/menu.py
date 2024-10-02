from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    """
    Sets the list of commands available to users in the bot's menu.
    """
    commands = [
        BotCommand(
            command="/start",
            description="Редактировать профиль"
        ),
        BotCommand(
            command="/blacklist",
            description="Черный список"
        ),
        BotCommand(
            command="/active",
            description="Активен ли аккаунт"
        ),
        BotCommand(
            command="/cancel",
            description="Отменить текущий диалог"
        ),
        BotCommand(
            command="/help",
            description="О чем этот бот"
        ),
    ]

    await bot.set_my_commands(commands)
