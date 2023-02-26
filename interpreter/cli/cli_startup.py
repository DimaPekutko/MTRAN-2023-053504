import os
import logging
from argparse import ArgumentParser

from interpreter.lexer.token_types import TOKENS_GROUPS
from interpreter.error import cli_error
from interpreter.lexer import tokenize_source
from interpreter.parser import Parser
from interpreter.semantics import SemanticAnalyzer
from interpreter.ast import AST_Printer
from interpreter.evaluation import *


def parse_args():
    """ Parsing args and return it """

    parser = ArgumentParser(description="Python based typed Interpreter.")
    parser.add_argument(dest="filename", type=str, help="Main file for interpretation")
    parser.add_argument("-L", "--log", action="store_true", help="Complete log of execution")


    return parser.parse_args()


def log_header(msg):
    columns, lines = os.get_terminal_size()
    print("")
    print("-" * columns)
    print(f"\n{msg.center(columns)}\n")
    print("-" * columns)
    print("")


def log_lexer(tokens, to_log=False):
    if not to_log:
        return
    groups = {
        "keywords": [], "operators": [], "marks": [], "literals": [], "identifiers": []
    }

    log_header("LEXER")

    for token in tokens:
        for key, group_tokens in TOKENS_GROUPS.items():
            if token.type in TOKENS_GROUPS[key]:
                groups[key].append(token)
                break
            
    for key, group_tokens in groups.items():
        print(f"\n\t{key}\n")
        for token in group_tokens:
            print(f" '{token.value}'  =>  {token.type.name}")


def log_parser(ast, to_log=False):
    if not to_log:
        return

    log_header("PARSER")
    printer = AST_Printer(ast)
    printer.print()


def log_semantics(scope_controller, to_log=False):
    if not to_log:
        return

    log_header("SEMANTICS")
    print(scope_controller)


def log_evaluation(to_log=False):
    if not to_log:
        return
    
    log_header("EVALUATION")


def run_main_loop(cli_args):
    """ Run main interpreter cycle if no cli errors """

    entry_file_name = os.path.abspath(cli_args.filename)
    if os.path.exists(entry_file_name) and os.path.isfile(entry_file_name):

        to_log = cli_args.log
        
        # lexer part
        tokens = tokenize_source(entry_file_name)
        log_lexer(tokens, to_log)
        # parser part
        parser = Parser(tokens)
        ast = parser.parse()
        log_parser(ast, to_log)
        # semantics part
        sem_analyzer = SemanticAnalyzer(ast)
        scope_controller = sem_analyzer.analyze()
        log_semantics(scope_controller, to_log)
        # evaluation
        log_evaluation(to_log)
        interpreter = EvaluationLoop(ast, scope_controller)
        interpreter.evaluate()


        
    else:
        cli_error(f"Can not find file with name '{entry_file_name}'")
