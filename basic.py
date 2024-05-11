from constants import *
from typing import List, Union, Tuple, Optional
import _tokens


# ERRORS

class Error:
    def __init__(self, error_name: str, details: str, pos_start: "Position", pos_end: "Position") -> None:
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self) -> str:
        return f"{self.error_name}: {self.details}\nFile {self.pos_start.file_name}, line {self.pos_start.line_number + 1}"


class IllegalCharError(Error):
    def __init__(self, details: str, pos_start: "Position", pos_end: "Position") -> None:
        super().__init__("Illegal Character", details, pos_start, pos_end)


# POSITION

class Position:
    def __init__(self, index: int, line_number: int, column_number: int, file_name: str, file_text: str) -> None:
        self.index = index
        self.line_number = line_number
        self.column_number = column_number
        self.file_name = file_name
        self.file_text = file_text

    def advance(self, current_char: str) -> "Position":
        self.index += 1
        self.column_number += 1

        if current_char == "\n":
            self.line_number += 1
            self.column_number = 0

        return self

    def copy(self):
        return Position(self.index, self.line_number, self.column_number, self.file_name, self.file_text)


# LEXER

class Lexer:
    def __init__(self, text: str, file_name: str) -> None:
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()

    def advance(self) -> None:
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.text):
            self.current_char = self.text[self.pos.index]
        else:
            self.current_char = None

    def make_tokens(self) -> Tuple[Union[List[_tokens.Token], List[None]], Optional[Error]]:
        tokens: list[_tokens.Token] = []

        while self.current_char is not None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "+":
                tokens.append(_tokens.Token(TOKEN_TYPE_PLUS))
                self.advance()
            elif self.current_char == "-":
                tokens.append(_tokens.Token(TOKEN_TYPE_MINUS))
                self.advance()
            elif self.current_char == "*":
                tokens.append(_tokens.Token(TOKEN_TYPE_MUL))
                self.advance()
            elif self.current_char == "/":
                tokens.append(_tokens.Token(TOKEN_TYPE_DIV))
                self.advance()
            elif self.current_char == "(":
                tokens.append(_tokens.Token(TOKEN_TYPE_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(_tokens.Token(TOKEN_TYPE_RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(f'"{char}"', pos_start, self.pos)

        return tokens, None

    def make_number(self) -> "_tokens.Token":
        num = ""
        dot_count = 0

        while self.current_char is not None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num += "."
            else:
                num += self.current_char
            self.advance()

        if dot_count:
            return _tokens.Token(TOKEN_TYPE_FLOAT, float(num))

        return _tokens.Token(TOKEN_TYPE_INT, int(num))




# RUN
def run(text: str, file_name: str):
    lexer = Lexer(text, file_name)
    tokens, error = lexer.make_tokens()

    return tokens, error
