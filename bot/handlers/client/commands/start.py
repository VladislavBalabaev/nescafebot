from enum import Enum
from random import randint
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

# from db.operations.user_profile import delete_everithing
from handlers.common.checks import checker
from handlers.client.email import send_email
from db.operations.messages import send_msg_user
from db.operations.users import update_user, find_user
from handlers.client.shared.keyboard import create_keyboard
from handlers.client.shared.contains import contains_command


router = Router()


class StartStates(StatesGroup):
    """
    State management for handling the registration process, including email verification, profile setup, 
    and program details.
    """
    EMAIL_GET = State()
    EMAIL_SET = State()
    NAME = State()
    AGE = State()
    PROGRAM_NAME = State()
    PROGRAM_YEAR = State()
    ABOUT = State()


class StartProgramNames(Enum):
    """
    Enum class representing available program names (BAE, MAE, MAF/MIF) for the registration process.
    """
    BAE = "BAE"
    MAE = "MAE"
    MAF = "MAF/MIF"

    @classmethod
    def has_value(cls, value):
        """
        Checks if the provided value is a valid program name.
        """
        return value in cls._value2member_map_


# @router.message(StateFilter(None), Command("d"))
# async def cmd_AAAAAA(message: types.Message, state: FSMContext):
#     await delete_everithing()


@router.message(StateFilter(None), Command("start"))
@checker
async def cmd_start(message: types.Message, state: FSMContext):
    """
    Handles the /start command. Initiates the registration process or allows users to update their profile 
    if they have already registered.
    """
    exist = await find_user(message.from_user.id, ["info.email"])
    exist = exist["info"]["email"]

    if not exist:
        await send_msg_user(message.from_user.id, 
                            "Привет!\nДобро пожаловать в бот Random Coffee для действующих студентов РЭШ, созданный студентами MAE'25 @vbalab и @Madfyre.\n\nВсё очень просто: раз в две недели, с учётом твоего чёрного списка, мы случайным образом подбираем тебе двух других студентов для встречи за кофе.\n\nДавай начнём с регистрации, это займёт минуту!")

        await send_msg_user(message.from_user.id, 
                            "Пожалуйста, укажи свой адрес электронной почты @nes.ru.\n\nЭто нужно, чтобы подтвердить, что ты студент РЭШ")

        await state.set_state(StartStates.EMAIL_GET)
    else:
        await send_msg_user(message.from_user.id, 
                            "Почта у тебя уже привязана, поэтому давай пройдемся по данным")

        await send_msg_user(message.from_user.id, 
                            "Как тебя зовут?")

        await state.set_state(StartStates.NAME)

    return


@router.message(StateFilter(StartStates.EMAIL_GET))
@checker
@contains_command
async def start_email_get(message: types.Message, state: FSMContext):
    """
    Collects the user's @nes.ru email address and sends a verification code if the email is valid.
    """
    if "@nes.ru" in message.text:
        await send_msg_user(message.from_user.id,
                            "Отлично, сейчас отправим тебе письмо с кодом подтверждения.\nПодожди секундочку...")

        code = str(randint(100000, 999999))

        await update_user(message.from_user.id,
                          {"cache.email": message.text, "cache.email_code": code})

        await send_email(message.text, f"Еще раз привет!\nТвой код для NEScafeBot: {code}.\nКод был отправлен для аккаунта @{message.from_user.username}")

        await send_msg_user(message.from_user.id, 
                            "Мы отправили тебе на почту код из 6 цифр.\nПожалуйста, введи его сюда")

        await state.set_state(StartStates.EMAIL_SET)
    else:
        await send_msg_user(message.from_user.id, 
                            "Это не @nes.ru адрес электронной почты 😕\n\nПожалуйста, введи правильный адрес",
                            fail=True)
    
    return


@router.message(StateFilter(StartStates.EMAIL_SET))
@checker
@contains_command
async def start_email_set(message: types.Message, state: FSMContext):
    """
    Verifies the email by checking the user's input against the sent verification code.
    """
    cache = await find_user(message.from_user.id, ["cache"])
    email_code = cache["cache"]["email_code"]

    if message.text.replace(' ', '') == email_code:
        email = cache["cache"]["email"]

        await update_user(message.from_user.id, 
                          {"info.email": email, "cache": {}})

        await send_msg_user(message.from_user.id, 
                            "Отлично!\nТвой адрес электронной почты успешно подтверждён и привязан к аккаунту")

        await send_msg_user(message.from_user.id, 
                            "Как тебя зовут? 😊")

        await state.set_state(StartStates.NAME)
    else:
        await send_msg_user(message.from_user.id, 
                            "Упс, неверный код😕\nПопробуй ещё раз.\n\nP.S. Если ты случайно указал не тот адрес электронной почты, введи /cancel и начни регистрацию заново с помощью команды /start.",
                            fail=True)

    return


@router.message(StateFilter(StartStates.NAME))
@checker
@contains_command
async def start_name(message: types.Message, state: FSMContext):
    """
    Collects the user's name and moves to the next step in the registration process.
    """
    if len(message.text) < 50 and len(message.text.split(" ")) <= 3:
        await update_user(message.from_user.id, 
                          {"info.written_name": message.text})

        await send_msg_user(message.from_user.id, 
                            "Сколько тебе лет?")

        await state.set_state(StartStates.AGE)
    else:
        await send_msg_user(message.from_user.id, 
                            "Кажется, это имя слишком длинное 😅",
                            fail=True)
    
    return


@router.message(StateFilter(StartStates.AGE))
@checker
@contains_command
async def start_age(message: types.Message, state: FSMContext):
    """
    Collects the user's age and verifies that it's a valid number within the acceptable range.
    """
    if message.text.isdigit() and int(message.text) >= 16 and int(message.text) <= 99:
        await update_user(message.from_user.id, 
                          {"info.age": message.text})

        keyboard = create_keyboard(StartProgramNames)

        await send_msg_user(message.from_user.id,
                            "Пожалуйста, выбери свою программу обучения из списка ниже",
                            reply_markup=keyboard)

        await state.set_state(StartStates.PROGRAM_NAME)
    else:
        await send_msg_user(message.from_user.id, 
                            "Хмм, это не похоже на возраст 😕\n\nПожалуйста, введи свой возраст цифрами",
                            fail=True)
    
    return


@router.message(StateFilter(StartStates.PROGRAM_NAME))
@checker
@contains_command
async def start_program_name(message: types.Message, state: FSMContext):
    """
    Collects the user's program name and ensures it's a valid option from the predefined list.
    """
    if StartProgramNames.has_value(message.text):
        await update_user(message.from_user.id, 
                          {"info.program.name": message.text})

        await send_msg_user(message.from_user.id,
                            "Теперь, выбери год программы (напр., 2023)",
                            reply_markup=types.ReplyKeyboardRemove())

        await state.set_state(StartStates.PROGRAM_YEAR)
    else:
        keyboard = create_keyboard(StartProgramNames)
        await send_msg_user(message.from_user.id,
                            "Пожалуйста, выбери один из предложенных вариантов 😊",
                            reply_markup=keyboard)

    return


@router.message(StateFilter(StartStates.PROGRAM_YEAR))
@checker
@contains_command
async def start_program_year(message: types.Message, state: FSMContext):
    """
    Collects the user's program year and ensures it's a valid number.
    """
    year = message.text

    if year.isdigit() and int(year) >= 1990 and int(year) < 9999:
        await update_user(message.from_user.id, 
                          {"info.program.year": year})

        await send_msg_user(message.from_user.id, 
                            "Расскажи о себе в нескольких предложениях.\nЭто поможет другим участникам узнать тебя лучше")

        await state.set_state(StartStates.ABOUT)
    else:
        await send_msg_user(message.from_user.id, 
                            "Это не похоже на год 😕\n\nПожалуйста, введи год в формате yyyy (например, 2023)",
                            fail=True)

    return


@router.message(StateFilter(StartStates.ABOUT))
@checker
@contains_command
async def start_about(message: types.Message, state: FSMContext):
    """
    Collects a short description from the user and finalizes the registration process.
    """
    if len(message.text) < 300:
        existed = await find_user(message.from_user.id, ["finished_profile"])
        existed = existed["finished_profile"]

        await update_user(message.from_user.id, 
                        {"info.about": message.text, 
                        "active_matching": "yes",
                        "finished_profile": "yes",})

        if existed == "yes":
            await send_msg_user(message.from_user.id,
                                "Твои данные обновлены! 🎉")
        else:
            await send_msg_user(message.from_user.id,
                                "Отлично, регистрация завершена! 🎉\nЕсли захочешь изменить свои данные, просто отправь команду /start.\n\nP.S. Повторно подтверждать адрес электронной почты не потребуется 😉")
            await send_msg_user(message.from_user.id, 
                                "Теперь расскажем подробнее о боте 😊\n\nКак уже говорилось, бот помогает случайным образом находить тебе компанию для кофе раз в две недели, чтобы познакомиться с новыми людьми или просто приятно провести время.\n\nПри распределении ты получишь свой смайл, например, 🐘. А также от 0 до 2 человек, которые тебе выпали, вместе с их смайлами.\n\nСмайл — это как приватный ключ и подтверждение того, что именно ты выпал другому человеку в Random Coffee.\nПоэтому ты можешь написать человеку только его смайл, и он сразу поймёт, по какому поводу ты пишешь!\n\nХотим уточнить, что распределение участников асимметричное. То есть, те люди, которые тебе выпадут, скорее всего не получат тебя")
            await send_msg_user(message.from_user.id, 
                                "[Если будут какие-либо пожелания и комментарии по поводу самого бота, пожалуйста, обращайся к создателям бота: @vbalab и @Madfyre]")

        await send_msg_user(message.from_user.id, 
                            "Также ты можешь добавить людей в свой черный список командой /blacklist, так пользователь никогда не попадется тебе, а ты пользователю.\n\nОт рандом кофе можно и отдохнуть, для этого есть /active, которое позволяет исключить твой аккаунт из последующих рандом кофе")
        await send_msg_user(message.from_user.id, 
                            "Enjoy!! ☕️😊")

        await state.clear()
    else:
        await send_msg_user(message.from_user.id, 
                            "Похоже, что описание слишком длинное 😅\n\nПожалуйста, попробуй написать покороче (до 300 символов)",
                            fail=True)

    return
