from aiogram import types


def create_keyboard(choices):
    """
    Creates a reply keyboard with the provided choices. Each choice is displayed as a button.
    The keyboard is resized for better display.
    """
    buttons = [[types.KeyboardButton(text=choice.value) for choice in choices]]
    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
