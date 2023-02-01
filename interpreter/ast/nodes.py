from enum import Enum
from abc import ABC

from interpreter.lexer.token import Token, TokenType

class AST_Node(ABC):
    def __init__(self, start_token: Token):
        self.start_token = start_token


class Literal_Node(AST_Node):
    def __init__(self, start_token: Token, value: any):
        super().__init__(start_token)
        self.value = value


class Var_Node(AST_Node):
    def __init__(self, start_token: Token, name: str):
        super().__init__(start_token)
        self.name = name


class Type_Node(AST_Node):
    def __init__(self, start_token: Token, name: str):
        super().__init__(start_token)
        self.name = name


class Binary_Op_Node(AST_Node):    
    def __init__(self, start_token: Token, left: AST_Node, right: AST_Node, token_type_op: TokenType):
        super().__init__(start_token)
        self.left = left
        self.right = right
        self.token_type_op = token_type_op


class Unary_Op_Node(AST_Node):    
    def __init__(self, start_token: Token, left: AST_Node, token_type_op: TokenType):
        super().__init__(start_token)
        self.left = left
        self.token_type_op = token_type_op


class Block_Node(AST_Node):
    def __init__(self, start_token: Token, statements: list[AST_Node]):
        super().__init__(start_token)
        self.statements = statements


class Statement_Node(AST_Node):    
    def __init__(self, start_token: Token, require_semicolon: bool = True):
        super().__init__(start_token)
        self.require_semicolon = require_semicolon


class Var_Decl_Node(Statement_Node):    
    def __init__(self, start_token: Token, name: str, type_node: Type_Node, value: AST_Node = None):
        super().__init__(start_token)
        self.name = name
        self.type_node = type_node
        self.value = value


class Var_Assign_Node(Statement_Node):    
    def __init__(self, start_token: Token, name: str, value: AST_Node):
        super().__init__(start_token)
        self.name = name
        self.value = value


class If_Else_Node(Statement_Node):
    def __init__(self, start_token: Token, condition: AST_Node, body: AST_Node, else_branch: AST_Node):
        super().__init__(start_token, False)
        self.condition = condition
        self.body = body
        self.else_branch = else_branch


class Loop_Node(Statement_Node):
    def __init__(self, start_token: Token, var: AST_Node, _range: tuple[AST_Node, AST_Node], step: AST_Node, body: AST_Node):
        super().__init__(start_token, False)
        self.var = var
        self.range = _range
        self.step = step
        self.body = body


class Func_Decl_Node(Statement_Node):
    def __init__(self, start_token: Token, name: str, params: list[Var_Decl_Node], ret_type_node: Type_Node, body: AST_Node):
        super().__init__(start_token, False)
        self.name = name
        self.params = params
        self.ret_type_node = ret_type_node
        self.body = body


class Func_Call_Node(Statement_Node):
    def __init__(self, start_token: Token, name: str, args: list[AST_Node]):
        super().__init__(start_token)
        self.name = name
        self.args = args


class Return_Node(Statement_Node):
    def __init__(self, start_token: Token, value: AST_Node):
        super().__init__(start_token)
        self.value = value


class Continue_Node(Statement_Node):
    def __init__(self, start_token: Token):
        super().__init__(start_token)


class Break_Node(Statement_Node):
    def __init__(self, start_token: Token):
        super().__init__(start_token)

