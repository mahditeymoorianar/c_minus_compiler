from enum import Enum


class TokenType(Enum):
    ERROR = -1
    NUM = 0
    ID = 1
    KEYWORD = 2
    SYMBOL = 3
    COMMENT = 4
    WHITESPACE = 5
