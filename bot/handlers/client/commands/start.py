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


router = Router()


class StartStates(StatesGroup):
    EMAIL_GET = State()
    EMAIL_SET = State()
    NAME = State()
    AGE = State()
    PROGRAM_NAME = State()
    PROGRAM_YEAR = State()
    ABOUT = State()


class StartProgramNames(Enum):
    BAE = "BAE"
    MAE = "MAE"
    MAF = "MAF/MIF"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


# @router.message(StateFilter(None), Command("d"))
# async def cmd_AAAAAA(message: types.Message, state: FSMContext):
#     await delete_everithing()


@router.message(StateFilter(None), Command("start"))
@checker
async def cmd_start(message: types.Message, state: FSMContext):
    exist = await find_user(message.from_user.id, ["info.email"])  # !!!!! check email
    exist = exist["info"]["email"]
    if not exist:
        if message.from_user.username is None:
            await message.answer("Данным ботом могут пользоваться только зарегестрированные в телеграм пользователи.")
            return

        await send_msg_user(message.from_user.id, 
                            "Привет!\nЭто бот random coffee для действующих студентов РЭШ созданный студентами MAE'25 @vbalab и @Madfyre.\n\nКонцепция бота очень простая, раз в две недели с учетом твоего черного списка пользователей мы случайным образом подбираем тебе двух пользователей бота, с которыми ты сможешь попить кофе.\n\nОб остальных подробностях поговорим позже, давай сначала тебя зарегистрируем")


    has_email = await find_user(message.from_user.id, ["info.email"])
    has_email = has_email["info"]["email"]

    if has_email:
        await send_msg_user(message.from_user.id, 
                            "Почта у тебя уже привязана, поэтому давай пройдемся по данным")

        await send_msg_user(message.from_user.id, 
                            "Как тебя зовут?")

        await state.set_state(StartStates.NAME)
    else:
        await send_msg_user(message.from_user.id, 
                            "Какая у тебя @nes.ru почта?\n\nОна нужна нам, чтобы мы могли подтвердить, что ты студент РЭШ")

        await state.set_state(StartStates.EMAIL_GET)
    
    return


@router.message(StateFilter(StartStates.EMAIL_GET))
@checker
async def start_email_get(message: types.Message, state: FSMContext):
    # TODO: "/" not in message.text

    if "@nes.ru" in message.text:
        await send_msg_user(message.from_user.id, 
                            "Секундочку, отправляем письмо")

        code = str(randint(100000, 999999))

        await update_user(message.from_user.id,
                          {"cache.email": message.text, "cache.email_code": code})

        await send_email(message.text, f"Еще раз привет!\nТвой код для NEScafeBot: {code}.\nКод был отправлен для аккаунта @{message.from_user.username}")

        await send_msg_user(message.from_user.id, 
                            "Мы отправили тебе на почту код из 6 цифр.\nНапиши его, пожалуйста, сюда")

        await state.set_state(StartStates.EMAIL_SET)
    else:
        await send_msg_user(message.from_user.id, 
                            "Это не почта РЭШ\nДавай заново",
                            fail=True)
    
    return


@router.message(StateFilter(StartStates.EMAIL_SET))
@checker
async def start_email_set(message: types.Message, state: FSMContext):
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
@checker
async def start_name(message: types.Message, state: FSMContext):
    if len(message.text) < 50 and len(message.text.split(" ")) <= 3:
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
@checker
async def start_age(message: types.Message, state: FSMContext):
    if message.text.isdigit() and int(message.text) >= 16 and int(message.text) <= 55:
        await update_user(message.from_user.id, 
                          {"info.age": message.text})

        keyboard = create_keyboard(StartProgramNames)

        await send_msg_user(message.from_user.id,
                            "Выбери свою программу",
                            reply_markup=keyboard)

        await state.set_state(StartStates.PROGRAM_NAME)
    else:
        await send_msg_user(message.from_user.id, 
                            "Это точно не возраст)\nДавай заново",
                            fail=True)
    
    return


@router.message(StateFilter(StartStates.PROGRAM_NAME))
@checker
async def start_program_name(message: types.Message, state: FSMContext):
    if StartProgramNames.has_value(message.text):
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
@checker
async def start_program_name(message: types.Message, state: FSMContext):
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
@checker
async def start_about(message: types.Message, state: FSMContext):
    if len(message.text) < 300:
        existed = await find_user(message.from_user.id, ["finished_profile"])
        existed = existed["finished_profile"]

        await update_user(message.from_user.id, 
                        {"info.about": message.text, 
                        "active_matching": "yes",
                        "finished_profile": "yes",})

        if existed == "yes":
            await send_msg_user(message.from_user.id,
                                "Данные профиля изменены!")
        else:
            await send_msg_user(message.from_user.id,
                                "Это все, что нам нужно!\nЕсли захочешь изменить что-либо о себе, просто напиши /start.\n\nP.S. Почту повторно подтверждать не придется)")
            await send_msg_user(message.from_user.id, 
                                "Теперь чуть подробнее расскажем о боте)\n\nКак уже говорилось, суть бота в том, чтобы раз в две недели подбирать случайным образом компаньона на кофе, для того, чтобы познакомиться или просто приятно провести время.\n\nВо время распределения тебе придет твой смайл, например, :gorilla:. А также от нуля до двух пользователей с их смайлами.\nТы можешь написать человеку только лишь его смайл и он сразу поймет, по какому поводу ты пишешь)")

        await send_msg_user(message.from_user.id, 
                            "Также ты можешь добавить людей в свой черный список командой /blacklist, так пользователь никогда не попадется тебе, а ты пользователю.\n\nОт рандом кофе можно и отдохнуть, для этого есть /active, которое позволяет исключить твой аккаунт из последующих рандом кофе")
        await send_msg_user(message.from_user.id, 
                            "Enjoy!!")

        await state.clear()
    else:
        await send_msg_user(message.from_user.id, 
                            "Слишком много написанного)\nДавай заново",
                            fail=True)

    return
