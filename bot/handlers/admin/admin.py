import logging
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram import Dispatcher, types, Router
from aiogram.filters.command import Command, CommandObject

from create_bot import bot
from configs.logs import logs_path
from configs.selected_ids import ADMINS
from handlers.common.addressing_errors import error_sender

router = Router()


class AdminFilter(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in ADMINS


@router.message(StateFilter(None), Command("admin_commands"), AdminFilter())
@error_sender
async def cmd_send_logs(message: types.Message, state: FSMContext):
    logging.info(f"Admin @{message.from_user.username} asked for his commands.")

    await message.answer("""/logs\n/see_messages @tg 30\n""")


@router.message(StateFilter(None), Command("logs"), AdminFilter())
@error_sender
async def cmd_send_logs(message: types.Message, state: FSMContext):
    logging.info(f"Admin @{message.from_user.username} asked for logs.")

    await message.answer_document(types.FSInputFile(logs_path))


@router.message(StateFilter(None), Command("see_messages"), AdminFilter())
@error_sender
async def cmd_send_chat_history(message: types.Message, state: FSMContext, command: CommandObject):
    """Like: /see_messages vbalab 20"""
    # logging.info(f"Admin @{message.from_user.username} ...")

    args = command.args.split()
    person_tg = args[0].replace('@', '')
    n_messages = int(args[1])

    await message.answer(f"# @{person_tg}'s last {n_messages} messages: #")

    # USING REDIS: get chat_id and last_message_id from @person_tg that is supplied in this function

    from_chat_id = 565279321
    last_message_id = 2344

    message_ids = reversed([last_message_id-i for i in range(n_messages)])

    await bot.copy_messages(chat_id=message.chat.id, from_chat_id=from_chat_id, message_ids=message_ids)


@router.message(StateFilter(None), Command("get_ids_CURRENT"))
@error_sender
async def cmd_send_chat_history(message: types.Message, state: FSMContext):
    await message.answer(f"ChatId: {str(message.chat.id)}, MessageId: {str(message.message_id)}")


def register_handlers_admin(dp: Dispatcher):
    dp.include_routers(router)
