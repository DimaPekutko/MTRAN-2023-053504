import os
from argparse import ArgumentParser

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
    
    return parser.parse_args()


def run_main_loop(cli_args):
    """ Run main interpreter cycle if no cli errors """

    entry_file_name = os.path.abspath(cli_args.filename)

    if os.path.exists(entry_file_name) and os.path.isfile(entry_file_name):
        # lexer part
        tokens = tokenize_source(entry_file_name)
        # parser part
        parser = Parser(tokens)
        ast = parser.parse()
        # printer
        printer = AST_Printer(ast)
        # printer.print()
        # semantics part
        sem_analyzer = SemanticAnalyzer(ast)
        scope_controller = sem_analyzer.analyze()
        # evaluation
        interpreter = EvaluationLoop(ast, scope_controller)
        interpreter.evaluate()


        
    else:
        cli_error(f"Can not find file with name '{entry_file_name}'")