import typing
import _tokens
import constants
import _errors

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

    def make_tokens(self) -> typing.Tuple[typing.Union[typing.List[_tokens.Token], typing.List[None]], typing.Optional["_errors.Error"]]:
        tokens: list[_tokens.Token] = []

        while self.current_char is not None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in constants.DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "+":
                tokens.append(_tokens.Token(_tokens.TokenType.PLUS))
                self.advance()
            elif self.current_char == "-":
                tokens.append(_tokens.Token(_tokens.TokenType.MINUS))
                self.advance()
            elif self.current_char == "*":
                tokens.append(_tokens.Token(_tokens.TokenType.MUL))
                self.advance()
            elif self.current_char == "/":
                tokens.append(_tokens.Token(_tokens.TokenType.DIV))
                self.advance()
            elif self.current_char == "(":
                tokens.append(_tokens.Token(_tokens.TokenType.LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(_tokens.Token(_tokens.TokenType.RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], _errors.IllegalCharError(f'"{char}"', pos_start, self.pos)

        return tokens, None

    def make_number(self) -> "_tokens.Token":
        num = ""
        dot_count = 0

        while self.current_char is not None and self.current_char in constants.DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num += "."
            else:
                num += self.current_char
            self.advance()

        if dot_count:
            return _tokens.Token(_tokens.TokenType.FLOAT, float(num))

        return _tokens.Token(_tokens.TokenType.INT, int(num))



