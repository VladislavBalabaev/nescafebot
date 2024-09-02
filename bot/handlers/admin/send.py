import logging
from aiogram import types

from create_bot import bot
from configs.logs import logs_path
from .matching.assignment import match
from configs.selected_ids import ADMINS


async def send_startup():
    logging.info("### Bot has started working! ###")

    for admin in ADMINS:
        await bot.send_message(admin, "Bot has started working!")


async def send_shutdown():
    logging.info("### Bot has finished working! ###")

    for admin in ADMINS:
        await bot.send_message(admin, "Bot has finished working!")
        await bot.send_document(admin, document=types.FSInputFile(logs_path))


async def send_matching():
    matched = match()
    matched = matched.set_index("user")

    for user in matched:
        await bot.send_message(user, "Привет!\nТвой смайл - {matched.loc[user, 'smile']}",)

        n = len(matched.loc[user, "assignments"])

        if n==0:
            await bot.send_message(
                user,
                f"В этот раз тебе не досталось тех, кому можно написать.\nВозможно, это потому что у тебя слишком много людей в черном списке.\n\nВерни кого-нибудь из него и в следующий раз шанс кого-нибудь получить будет больше",
            )
        elif n==1:
            await bot.send_message(
                user,
                f"Тебе выпал один человек, которому ты можешь написать, это - @{matched.loc[user, 'assignments'][0]}.\n\nТы можешь написать ему его смайл - {matched.loc[matched.loc[user, 'assignments'][0], 'smile']}, он сразу поймет, что выпал тебе на кофе)",
            )
        elif n==2:
            await bot.send_message(
                user,
                f"Тебе выпали двое человек, которым ты можешь написать, это - @{matched.loc[user, 'assignments'][0]} со смайлом {matched.loc[matched.loc[user, 'assignments'][0], 'smile']}, а также @{matched.loc[user, 'assignments'][0]} со смайлом {matched.loc[matched.loc[user, 'assignments'][0], 'smile']}.\n\nТы можешь написать им их смайл, они сразу поймут, что выпали тебе на кофе)",
            )
