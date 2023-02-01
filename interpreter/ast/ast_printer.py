from .nodes import *
from .traverse import TreeVisitor


class AST_Printer(TreeVisitor):

    def __init__(self, ast: AST_Node):
        super().__init__(ast)
        self.silent = False

    def visit_literal(self, node):
        self.__print(f"Literal '{node.value}'")

    def visit_var(self, node):
        self.__print(f"Variable '{node.name}'")

    def visit_type(self, node):
        self.__print(f"Type '{node.name}'")

    def visit_binop(self, node):
        self.__print(f"BinOp {node.token_type_op}")
        self.visit_node(node.left)
        self.visit_node(node.right)

    def visit_unop(self, node):
        self.__print(f"UnOp {node.token_type_op}")
        self.visit_node(node.left)

    def visit_var_decl(self, node):
        self.__print(f"VarDecl '{node.name}'")
        self.visit_node(node.type_node)
        if node.value:
            self.visit_node(node.value)

    def visit_var_assign(self, node):
        self.__print(f"VarAssign '{node.name}'")
        self.visit_node(node.value)

    def visit_if_else(self, node):
        self.__print(f"If")

        if node.condition:
            self.__print(f" IfCondition:")
            self.visit_node(node.condition)
            
        self.__print(f" IfBody:")
        self.visit_node(node.body)

        if node.else_branch:
            self.__print(f" IfElse:")
            self.visit_node(node.else_branch)
        
    def visit_loop(self, node):
        self.__print(f"Loop")
        
        if node.var:
            self.__print(f" ItVar")
            self.visit_node(node.var)
        if node.range:
            self.__print(f" ItRange")
            self.visit_node(node.range[0])
            self.visit_node(node.range[1])
        if node.step:
            self.__print(f" ItStep")
            self.visit_node(node.step)

        self.__print(f" ItBody")        
        self.visit_node(node.body)
    
    def visit_func_decl(self, node):
        self.__print(f"FunctionDecl '{node.name}'")
        self.visit_node(node.ret_type_node)
        
        self.__print(f" FuncParams")
        for param in node.params:
            self.visit_node(param)

        self.__print(f" FuncBody")
        self.visit_node(node.body)

    def visit_func_call(self, node):
        self.__print(f"FunctionCall '{node.name}'")
        self.__print(f" FuncCallArgs")
        for arg in node.args:
            self.visit_node(arg)

    def visit_return(self, node):
        self.__print(f"Return")
        self.visit_node(node.value)

    def visit_continue(self, node):
        self.__print(f"Continue")

    def visit_break(self, node):
        self.__print(f"Break")

    def visit_block(self, node):
        self.__print(f"Block")
        for stm in node.statements:
            self.visit_node(stm)

    def __print(self, message: str):
        """ Prints messages with offset related to depth """

        if self.silent:
            return
            
        length = (self.depth - 1) 
        offset = "  " * length if length else ""
        print(f"{offset}{message}")

    def print(self, silent: bool = False):
        self.silent = silent
        self.traverse()