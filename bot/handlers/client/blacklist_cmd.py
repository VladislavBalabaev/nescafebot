import asyncio
import logging
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup

from handlers.common.addressing_errors import error_sender


router = Router()


class blacklist_states(StatesGroup):
    after_start_cmd = State()

    blacklist = State()

    block_person = State()
    after_block_person = State()

    select_programs_year = State()
    block_program = State()
    after_block_program = State()


@router.message(StateFilter(blacklist_states.after_start_cmd))
@error_sender
async def notify_capabilities(message: types.Message, state: FSMContext):
    raise NotImplementedError


@router.message(StateFilter(None), Command("blacklist_add"))
@error_sender
async def cmd_blacklist(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} has started to write to his blacklist.")

    await state.set_state(blacklist_states.blacklist)

    buttons = [[
            types.KeyboardButton(text="Человека"),
            types.KeyboardButton(text="Программа'год")
            ]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


    await message.answer("Сейчас ты можешь добавить какого-либо конкретного человека через его @tg или всех людей с какой-либо программы'года в черный спискок.\n\nТаким образом, люди из черного списка не будут предлагаться тебе и ты не будешь предложен им на следующем кофе.")

    await message.answer(
        "Выбери, добавляем в черный список:", 
        reply_markup=keyboard
        )


@router.message(StateFilter(blacklist_states.blacklist), F.text == "Человека")
@router.message(StateFilter(blacklist_states.after_block_person), F.text == "Да")
@error_sender
async def blacklist_select_person(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} chose to block person.")

    await state.set_state(blacklist_states.block_person)

    await message.answer(
        "Напиши, кого добавить в чс", 
        reply_markup=types.ReplyKeyboardRemove()
        )


@router.message(StateFilter(blacklist_states.block_person))
@error_sender
async def blacklist_block_person(message: types.Message, state: FSMContext):
    person = message.text.strip().replace(' ', '').replace('@', '') # TODO: add different variants

    logging.info(f"User @{message.from_user.username} added @{person} to his blacklist.")

    await state.set_state(blacklist_states.after_block_person)

    # TODO: add written @tg to his REDIS blacklist

    await message.answer(f"Добавили в твой черный список.\nНа следующем кофе @{person} тебе не попадется!")


    buttons = [[
        types.KeyboardButton(text="Да"),
        types.KeyboardButton(text="Нет")
        ]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await message.answer(
        f"Хочешь добавить @tg ещё кого-нибудь?", 
        reply_markup=keyboard
        )


@router.message(StateFilter(blacklist_states.blacklist), F.text == "Программа'год")
@router.message(StateFilter(blacklist_states.after_block_program), F.text == "Да")
@error_sender
async def blacklist_select_program(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} chose to block program'year.")

    await state.set_state(blacklist_states.select_programs_year)

    buttons = [[
        types.KeyboardButton(text="MAE"),
        types.KeyboardButton(text="MAF/MIF"),
        types.KeyboardButton(text="BAE")
        ]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await message.answer(
        "Для начала, выбери, какую программу добавляем?", 
        reply_markup=keyboard
        )


@router.message(StateFilter(blacklist_states.select_programs_year))
@error_sender
async def blacklist_select_year(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} selected {message.text} to block.")
    
    await state.set_state(blacklist_states.block_program)
    await state.set_data({"program": message.text})
    
    await message.answer(
        "Теперь, выбери год программы (напр., 2023)",
        reply_markup=types.ReplyKeyboardRemove()
        )


@router.message(StateFilter(blacklist_states.block_program))
@error_sender
async def blacklist_block_program(message: types.Message, state: FSMContext): 
    year = message.text.strip().replace(' ', '')

    if not year.isdigit() or int(year) < 1990:
        await message.answer("Это не год.\nВыбери год программы, которую хочешь добавить в черный список в формате yyyy (напр., 2023)")
        return

    data = await state.get_data()
    program_year = f"{data['program']}'{year}"

    logging.info(f"User @{message.from_user.username} added {program_year} to blacklist.")

    await state.set_state(blacklist_states.after_block_program)

    # TODO: add written program'year to his REDIS blacklist

    await message.answer(f"Добавили в твой черный список.\nНа следующем кофе люди с {program_year} тебе не попадутся!")


    buttons = [[
        types.KeyboardButton(text="Да"),
        types.KeyboardButton(text="Нет")
        ]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await message.answer(
        f"Хочешь добавить еще одну программу'год?", 
        reply_markup=keyboard
        )


@router.message(StateFilter(blacklist_states.after_block_person), F.text == "Нет")
@router.message(StateFilter(blacklist_states.after_block_program), F.text == "Нет")
@error_sender
async def blacklist_end(message: types.Message, state: FSMContext):
    logging.info(f"User @{message.from_user.username} chose not to continue blocking.")

    await state.clear()

    await message.answer("Хорошо", reply_markup=types.ReplyKeyboardRemove())
