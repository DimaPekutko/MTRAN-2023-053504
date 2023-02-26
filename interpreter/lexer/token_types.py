from enum import Enum


class TokenType(Enum):
    INT_LITERAL = 1,
    FLOAT_LITERAL = 2,
    STR_LITERAL = 3,
    SEMICOLON = 4,
    DOUBLE_QUOTE = 5,
    PLUS_OP = 6,
    MINUS_OP = 7,
    MULT_OP = 8,
    DIV_OP = 9,
    ASSIGN_OP = 10,
    LEFT_PAR = 11,
    RIGHT_PAR = 12,
    LEFT_BRACE = 13,
    RIGHT_BRACE = 14,
    LEFT_BRACKET = 15,
    RIGHT_BRACKET= 16,
    COMMA = 17,
    PIPE = 18,
    SPACE = 20

    LOOP_KWD = 21,
    IF_KWD = 22,
    IFELSE_KWD = 23,
    ELSE_KWD = 24,
    DEF_KWD = 25,
    RANGE_MARK = 26,
    EXCL_MARK = 27,
    QUEST_MARK = 28,
    RET_TYPE_MARK = 29,
    NEXT_KWD = 30,
    STOP_KWD = 31,

    GT_OP = 32,
    GTE_OP = 33,
    LT_OP = 34,
    LTE_OP = 35,
    EQ_OP = 36,
    NEQ_OP = 37,

    NOT_OP = 38,
    AND_OP = 39,
    OR_OP = 40

    LINE_COMMENT = 41,

    IDENTIFIER = 99,

    EOF = 100


TOKEN_TYPES_REGEXES = {
    TokenType.FLOAT_LITERAL : r"(\d+)(\.)(\d+)",
    TokenType.INT_LITERAL   : r"\d+",
    TokenType.GTE_OP        : r"\>\=",
    TokenType.LTE_OP        : r"\<\=",
    TokenType.EQ_OP         : r"\=\=",
    TokenType.GT_OP         : r"\>",
    TokenType.LT_OP         : r"\<",
    TokenType.NEQ_OP        : r"\!\=",
    TokenType.NOT_OP        : r"\bnot\b",
    TokenType.AND_OP        : r"\band\b",
    TokenType.OR_OP         : r"\bor\b",
    TokenType.RET_TYPE_MARK : r"\-\>",
    TokenType.SEMICOLON     : r"\;",
    TokenType.DOUBLE_QUOTE  : r'\"',
    TokenType.PLUS_OP       : r"\+",
    TokenType.MINUS_OP      : r"\-",
    TokenType.MULT_OP       : r"\*",
    TokenType.DIV_OP        : r"\/",
    TokenType.ASSIGN_OP     : r"\=",
    TokenType.LEFT_PAR      : r"\(",
    TokenType.RIGHT_PAR     : r"\)",
    TokenType.LEFT_BRACE    : r"\{",
    TokenType.RIGHT_BRACE   : r"\}",
    TokenType.LEFT_BRACKET  : r"\[",
    TokenType.RIGHT_BRACKET : r"\]",
    TokenType.COMMA         : r"\,",
    TokenType.PIPE          : r"\|",
    TokenType.SPACE         : r" ",
    TokenType.LOOP_KWD      : r"\bloop\b",
    TokenType.IF_KWD        : r"\bif\b",
    TokenType.IFELSE_KWD    : r"\belse if\b",
    TokenType.ELSE_KWD      : r"\belse\b",
    TokenType.DEF_KWD       : r"\bdef\b",
    TokenType.NEXT_KWD      : r"\bnext\b",
    TokenType.STOP_KWD      : r"\bstop\b",
    TokenType.RANGE_MARK    : r"\.\.",
    TokenType.EXCL_MARK     : r"\!",
    TokenType.QUEST_MARK    : r"\?",
    TokenType.LINE_COMMENT  : r"\#",
    TokenType.IDENTIFIER    : r"([A-Za-z\_\d+])+",
    TokenType.STR_LITERAL   : r"(?!x)x", # match nothing
    TokenType.EOF           : r"(?!x)x", # match nothing
}


TOKENS_GROUPS = {
    "keywords": [
        TokenType.IF_KWD, TokenType.ELSE_KWD, TokenType.IFELSE_KWD, TokenType.LOOP_KWD, TokenType.DEF_KWD,
        TokenType.NEXT_KWD, TokenType.STOP_KWD
    ],
    "operators": [
        TokenType.PLUS_OP, TokenType.MINUS_OP, TokenType.MULT_OP, TokenType.DIV_OP, TokenType.ASSIGN_OP,
        TokenType.EQ_OP, TokenType.NEQ_OP, TokenType.AND_OP, TokenType.NOT_OP, TokenType.OR_OP,
        TokenType.GT_OP, TokenType.GTE_OP, TokenType.LT_OP, TokenType.LTE_OP
    ],
    "marks": [
        TokenType.RANGE_MARK, TokenType.EXCL_MARK, TokenType.RET_TYPE_MARK, TokenType.QUEST_MARK
    ],
    "literals": [
        TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL, TokenType.STR_LITERAL
    ],
    "identifiers": [
        TokenType.IDENTIFIER
    ]
}