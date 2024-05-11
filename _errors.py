import _lexer
# ERRORS

class Error:
    def __init__(self, error_name: str, details: str, pos_start: "_lexer.Position", pos_end: "_lexer.Position") -> None:
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self) -> str:
        return f"{self.error_name}: {self.details}\nFile {self.pos_start.file_name}, line {self.pos_start.line_number + 1}"


class IllegalCharError(Error):
    def __init__(self, details: str, pos_start: "_lexer.Position", pos_end: "_lexer.Position") -> None:
        super().__init__("Illegal Character", details, pos_start, pos_end)

