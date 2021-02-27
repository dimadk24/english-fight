import re


def snake_case(string: str) -> str:
    return re.sub('(?!^)([A-Z]+)', r'_\1', string).lower()
