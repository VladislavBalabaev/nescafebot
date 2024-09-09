from aiogram import types


def create_keyboard(choices):
    buttons = [[types.KeyboardButton(text=choice.value) for choice in choices]]
    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
