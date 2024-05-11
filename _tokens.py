# TOKENS

class TokenType:
    INT = "INT"
    FLOAT = "FLOAT"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"

class Token:
    def __init__(self, token_type: str, value: str = None):
        self._type = token_type
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f"{self._type}:{self.value}"
        return f"{self._type}"
