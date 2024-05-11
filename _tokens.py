# TOKENS

class Token:
    def __init__(self, token_type: str, value: str = None):
        self.token_type = token_type
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f"{self.token_type}:{self.value}"
        return f"{self.token_type}"
