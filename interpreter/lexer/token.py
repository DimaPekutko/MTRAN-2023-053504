from .token_types import TokenType


class TokenPos():
    def __init__(self, row: int, col: int, filename: str):
        self.row = row
        self.col = col
        self.filename = filename


class Token():
    def __init__(self, ttype: TokenType, value: any, tpos: TokenPos):
        self.type = ttype
        self.value = value
        self.pos = tpos