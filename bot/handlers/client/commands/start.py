import asyncio
from random import randint
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from ..email import send_email
from db.operations.profile import create_user
from db.operations.users import update_user, find_user
from handlers.common.addressing_errors import error_sender
from db.operations.messages import send_msg_user, recieve_msg_user


router = Router()


class StartStates(StatesGroup):
    EMAIL_GET = State()
    EMAIL_SET = State()
    NAME = State()
    AGE = State()
    PROGRAM_NAME = State()
    PROGRAM_YEAR = State()
    ABOUT = State()


@router.message(StateFilter(None), Command("start"))
@error_sender
async def cmd_start(message: types.Message, state: FSMContext):
    # await delete_everithing()

    exists = await find_user(message.from_user.id, ["_id"])

    if exists:
        await recieve_msg_user(message)

        await send_msg_user(message.from_user.id, 
                            "Почта у тебя уже привязана, поэтому давай пройдемся по данным")

        await send_msg_user(message.from_user.id, 
                            "Как тебя зовут?")

        await state.set_state(StartStates.NAME)
    else:
        await create_user(message)

        await recieve_msg_user(message)

        await send_msg_user(message.from_user.id, 
                            "Привет!\nЭто бот random coffee для действующих студентов РЭШ созданный студентами MAE'25 @vbalab и @Madfyre.\n\nКонцепция бота очень простая, раз в две недели с учетом твоего черного списка пользователей мы случайным образом подбираем тебе двух пользователей бота, с которыми ты сможешь попить кофе.\n\nОб остальных подробностях поговорим позже, давай сначала тебя зарегистрируем")

        await asyncio.sleep(1)
        await send_msg_user(message.from_user.id, 
                            "Какая у тебя @nes.ru почта?\n\nОна нужна нам, чтобы мы могли подтвердить, что ты студент РЭШ")

        await state.set_state(StartStates.EMAIL_GET)
    
    return


@router.message(StateFilter(StartStates.EMAIL_GET))
@error_sender
async def cmd_start(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    if "@nes.ru" in message.text:
        await send_msg_user(message.from_user.id, 
                            "Секундочку, отправляем письмо")

        code = str(randint(100000, 999999))

        await update_user(message.from_user.id,
                        {"cache.email": message.text, "cache.email_code": code})

        await send_email(message.text, f"Еще раз ривет!\nТвой код для NEScafeBot: {code}.\nКод был отправлен для аккаунта @{message.from_user.username}")

        await send_msg_user(message.from_user.id, 
                            "Мы отправили тебе на почту код из 6 цифр.\nНапиши его, пожалуйста, сюда")

        await state.set_state(StartStates.EMAIL_SET)
    else:
        await send_msg_user(message.from_user.id, 
                            "Это не почта РЭШ\nДавай заново",
                            fail=True)
    
    return


@router.message(StateFilter(StartStates.EMAIL_SET))
@error_sender
async def cmd_start(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    cache = await find_user(message.from_user.id, ["cache"])
    email_code = cache["cache"]["email_code"]

    if message.text.replace(' ', '') == email_code:
        email = cache["cache"]["email"]

        await update_user(message.from_user.id, 
                          {"info.email": email, "cache": {}})

        await send_msg_user(message.from_user.id, 
                            "Отлично!\nПривязали почту к твоему аккаунту")

        await send_msg_user(message.from_user.id, 
                            "Как тебя зовут?")

        await state.set_state(StartStates.NAME)
    else:
        await send_msg_user(message.from_user.id, 
                            "Код неверный)\nДавай заново",
                            fail=True)
    
    return


@router.message(StateFilter(StartStates.NAME))
@error_sender
async def start_name(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    if len(message.text) < 50:
        await update_user(message.from_user.id, 
                          {"info.written_name": message.text})

        await send_msg_user(message.from_user.id, 
                            "Сколько тебе лет?")

        await state.set_state(StartStates.AGE)
    else:
        await send_msg_user(message.from_user.id, 
                            "Слишком длинное имя)\nДавай заново",
                            fail=True)
    
    return


@router.message(StateFilter(StartStates.AGE))
@error_sender
async def start_age(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    if message.text.isdigit():
        await update_user(message.from_user.id, 
                          {"info.age": message.text})

        buttons = [[
            types.KeyboardButton(text="BAE"),
            types.KeyboardButton(text="MAE"),
            types.KeyboardButton(text="MAF/MIF"),
            ]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

        await send_msg_user(message.from_user.id,
                            "Выбери свою программу",
                            reply_markup=keyboard)

        await state.set_state(StartStates.PROGRAM_NAME)
    else:
        await send_msg_user(message.from_user.id, 
                            "Это было не число)\nДавай заново",
                            fail=True)
    
    return


@router.message(StateFilter(StartStates.PROGRAM_NAME))
@error_sender
async def select_program_name(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    if message.text in ["BAE", "MAE", "MAF/MIF"]:
        await update_user(message.from_user.id, 
                        {"info.program.name": message.text})

        await send_msg_user(message.from_user.id,
                            "Теперь, выбери год программы (напр., 2023)",
                            reply_markup=types.ReplyKeyboardRemove())

        await state.set_state(StartStates.PROGRAM_YEAR)
    else:
        await send_msg_user(message.from_user.id,
                            "Выбери из предложенных")

    return


@router.message(StateFilter(StartStates.PROGRAM_YEAR))
@error_sender
async def select_program_year(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    year = message.text

    if year.isdigit() and int(year) >= 1990 and int(year) < 9999:
        await update_user(message.from_user.id, 
                        {"info.program.year": year})

        await send_msg_user(message.from_user.id, 
                            "Напиши о себе в паре предложений")

        await state.set_state(StartStates.ABOUT)
    else:
        await send_msg_user(message.from_user.id, 
                            "Это не год.\nВыбери год программы, которую хочешь добавить в черный список в формате yyyy (напр., 2009)",
                            fail=True)

    return


@router.message(StateFilter(StartStates.ABOUT))
@error_sender
async def start_about(message: types.Message, state: FSMContext):
    await recieve_msg_user(message)

    await update_user(message.from_user.id, 
                    {"info.about": message.text})

    await send_msg_user(message.from_user.id, 
                        "Это все, что нам нужно!\nЕсли захочешь изменить что-либо о себе, просто напиши /start.\n\nP.S. Почту повторно подтверждать не придется)")

    await send_msg_user(message.from_user.id, 
                        "Теперь чуть подробнее расскажем о боте")

    await state.clear()

    return
