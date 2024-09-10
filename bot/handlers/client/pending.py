import logging
from create_bot import bot
from handlers.common.addressing_errors import error_sender


@error_sender
async def notify_users_with_pending_updates():
    updates = await bot.get_updates(offset=None, timeout=5)

    notified_users = set()

    for update in updates:
        if update.message:
            user_id = update.message.from_user.id
            logging.info(f"_id='{user_id}'   was pending \033[91m[FAIL]\033[0m: {repr(update.message.text)}")

            if user_id not in notified_users:
                await bot.send_message(user_id, 
                                   "Бот был неактивен, но сейчас еще как!\nПопробуй еще раз, пожалуйста")

                notified_users.add(user_id)

    await bot.get_updates(offset=updates[-1].update_id + 1 if updates else None)        # drop pending updates

    return
