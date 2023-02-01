
def cli_error(message: str):
    """ Throws cli error """

    print("Error occured!")
    print(f"    {message}")
    exit(1)


def analysis_error_template(message: str, code_fragment: str, row: int, col: int, filename: str):
    print(f"    {message}")
    print(f"    in file '{filename}'")
    print(f"    -> '{code_fragment}...' at pos [{row}:{col}].")


def syntax_error(*args):
    """ Throws syntax error """

    print("Syntax error occured")
    analysis_error_template(*args)
    exit(1)


def semantic_error(*args):
    """ Throws semantic error """

    print("Semantic error occured")
    analysis_error_template(*args)
    exit(1)