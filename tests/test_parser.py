from interpreter.lexer import tokenize_source
from interpreter.parser import Parser
from interpreter.ast import *


EXPECTED_NODE_TYPES = [
    Block_Node,
    Func_Decl_Node,
    Type_Node,
    Var_Decl_Node,
    Type_Node,
    Block_Node,
    Func_Decl_Node,
    Type_Node,
    Block_Node,
    Func_Decl_Node,
    Type_Node,
    Var_Decl_Node,
    Type_Node,
    Var_Decl_Node,
    Type_Node,
    Block_Node,
    Var_Decl_Node,
    Type_Node,
    Literal_Node,
    Var_Decl_Node,
    Type_Node,
    Loop_Node,
    Var_Node,
    Var_Node,
    Literal_Node,
    Block_Node,
    Loop_Node,
    Block_Node,
    If_Else_Node,
    Binary_Op_Node,
    Var_Node,
    Var_Node,
    Block_Node,
    Continue_Node,
    If_Else_Node,
    Binary_Op_Node,
    Var_Node,
    Func_Call_Node,
    Block_Node,
    Break_Node,
    If_Else_Node,
    Block_Node,
    Return_Node,
    Literal_Node,
    If_Else_Node,
    Binary_Op_Node,
    Binary_Op_Node,
    Binary_Op_Node,
    Var_Node,
    Literal_Node,
    Literal_Node,
    Binary_Op_Node,
    Var_Node,
    Func_Call_Node,
    Literal_Node,
    Literal_Node,
    Block_Node,
    Var_Decl_Node,
    Type_Node,
    Binary_Op_Node,
    Unary_Op_Node,
    Literal_Node,
    Binary_Op_Node,
    Binary_Op_Node,
    Literal_Node,
    Literal_Node,
    Binary_Op_Node,
    Literal_Node,
    Binary_Op_Node,
    Literal_Node,
    Unary_Op_Node,
    Literal_Node,
]


def test_parser_py():
    tokens = tokenize_source("tests/test_parser.txt")
    ast = Parser(tokens).parse() 
    
    printer = AST_Printer(ast)
    printer.print(True)
    
    nodes = printer.path

    assert len(nodes) == len(EXPECTED_NODE_TYPES)

    for i in range(len(nodes)):
        assert type(nodes[i]) == EXPECTED_NODE_TYPES[i]
    