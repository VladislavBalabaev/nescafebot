from .checks import text_checker
from .addressing_errors import error_sender

def checker(f):
    return error_sender(text_checker(f))
