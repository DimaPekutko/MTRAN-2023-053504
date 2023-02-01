import re
from .token_types import TokenType, TOKEN_TYPES_REGEXES
from .token import Token, TokenPos
from interpreter.error import syntax_error


_current_file_name = ""
_string_token = None


def _lex_line(source_code_line: str, line_number: int):
    """ Tokenize code line into tokens """
    
    global _current_file_name
    global _string_token

    if _string_token:
        _string_token.value += "\n"

    line = source_code_line
    col_number = 0
    tokens = []

    while (len(line) > 0):
        # string mode parsing
        if _string_token:
            regex = TOKEN_TYPES_REGEXES[TokenType.DOUBLE_QUOTE]
            match_res = re.search(regex, line)
            # matched
            if match_res and match_res.start() == 0:
                tokens.append(_string_token)
                line = line[match_res.end():]
                _string_token = None
            else:
                _string_token.value += line[0]
                line = line[1:]
            continue

        # normal mode parsing
        found = False
        for token_type, regex in TOKEN_TYPES_REGEXES.items():
            match_res = re.search(regex, line)
            # matched
            if match_res and match_res.start() == 0:
                found = True
                start = match_res.start()
                end = match_res.end()
                tpos = TokenPos(line_number, col_number, _current_file_name)

                token_value = line[start : end]
                line = line[end:]
                

                # if string start|end
                if token_type == TokenType.DOUBLE_QUOTE:
                    if not _string_token:
                        _string_token = Token(TokenType.STR_LITERAL, "", tpos)
                        break;

                token = Token(token_type, token_value, tpos)
                tokens.append(token)
                col_number += (end - start)

                # if comment
                if token_type == TokenType.LINE_COMMENT:
                    token.value = line
                    return tokens

                break;
        if not found:
            syntax_error(
                "Undefined token found!", 
                f"{line[0:5]}",
                line_number, 
                col_number,
                _current_file_name
            )

    return tokens


def tokenize_source(filename: str):
    """ Return source code splited into tokens if no lexical errors """

    global _current_file_name
    _current_file_name = filename

    lines_count = 1
    tokens = []

    with open(filename, "r") as file:
        for line in file:
            tokens += _lex_line(line.strip(), lines_count)
            lines_count += 1


    if _string_token:
        syntax_error(
            "Unclosed string literla found", f'"{_string_token.value}',
            _string_token.pos.row, _string_token.pos.col,_string_token.pos.filename
        )

    # eof token
    tokens.append(Token(
        TokenType.EOF, "",
        TokenPos(lines_count, 0, filename)
    ))

    return tokens