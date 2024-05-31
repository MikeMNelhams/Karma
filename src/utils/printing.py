import os


class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colour_print_string_header(phrase: str) -> str:
    return f"{PrintColors.HEADER}{phrase}{PrintColors.ENDC}"


def colour_blue(phrase: str) -> str:
    return f"{PrintColors.OKBLUE}{phrase}{PrintColors.ENDC}"


def colour_green(phrase: str) -> str:
    return f"{PrintColors.OKGREEN}{phrase}{PrintColors.ENDC}"


def colour_cyan(phrase: str) -> str:
    return f"{PrintColors.OKCYAN}{phrase}{PrintColors.ENDC}"


def colour_warning(phrase: str) -> str:
    return f"{PrintColors.WARNING}{phrase}{PrintColors.ENDC}"


def print_row(number_of_chars: int=50, char: str= '-') -> None:
    print(char * number_of_chars)
    return None


def print_top_and_bottom_rows(func: callable, char='-', number_of_chars: int = 40) -> callable:
    def wrapper(*args, **kwargs):
        print_row(char, number_of_chars)
        func(*args, **kwargs)
        print_row(char, number_of_chars)

    return wrapper


def clear_all_text() -> None:
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    return None
