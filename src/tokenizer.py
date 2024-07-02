from dataclasses import dataclass
from enum import Enum, auto
from typing import Any
from string import digits
import logging

logging.basicConfig(format='%(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('Tokenizer')
logger.setLevel(logging.INFO)


class TokenType(Enum):
    INT = auto()
    PLUS = auto()
    MINUS = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: Any = None


class Tokenizer:

    def __init__(self, code: str) -> None:
        self.code = code
        self.ptr: int = 0

    def __str__(self):
        return f'{self.code}'

    def __iter__(self):
        while (token := self.next_token()).type != TokenType.EOF:
            yield token
        yield token

    def next_token(self) -> Token:
        while self.ptr < len(self.code) and self.code[self.ptr] == " ":
            self.ptr += 1

        if self.ptr == len(self.code):
            return Token(TokenType.EOF)

        char = self.code[self.ptr]
        self.ptr += 1
        if char == "+":
            return Token(TokenType.PLUS)
        elif char == "-":
            return Token(TokenType.MINUS)
        elif char in digits:
            return Token(TokenType.INT, int(char))
        else:
            raise RuntimeError(f"Can't tokenize {char!r}.")


if __name__ == '__main__':
    x = Tokenizer('3 3 3 + 5 5 5 - - -')
    logger.info(x)
    for tok in x:
        logger.info(f'\t{tok.type}, {tok.value}')