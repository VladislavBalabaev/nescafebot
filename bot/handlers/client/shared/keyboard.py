from aiogram import types


def create_keyboard(choices):
    """
    Creates a reply keyboard with the provided choices. Each choice is displayed as a button.
    The keyboard is resized for better display. A maximum of 3 buttons is allowed per row.
    """
    max_buttons_per_row = 3

    choices_list = list(choices)

    buttons = [
        [types.KeyboardButton(text=choice.value) for choice in choices_list[i:i + max_buttons_per_row]]
        for i in range(0, len(choices_list), max_buttons_per_row)
    ]
    
    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
