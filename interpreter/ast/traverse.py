from abc import ABC, abstractmethod

from .nodes import *


class TreeVisitor(ABC):
    """ Abstract class for traversing nodes of AST """        

    def __init__(self, ast: AST_Node):
        self.nodes_handlers = {
            Literal_Node    : self.visit_literal,
            Var_Node        : self.visit_var,
            Type_Node       : self.visit_type,
            Binary_Op_Node  : self.visit_binop,
            Unary_Op_Node   : self.visit_unop,
            Var_Decl_Node   : self.visit_var_decl,
            Var_Assign_Node : self.visit_var_assign,
            Block_Node      : self.visit_block,
            If_Else_Node    : self.visit_if_else,
            Loop_Node       : self.visit_loop,
            Func_Decl_Node  : self.visit_func_decl,
            Func_Call_Node  : self.visit_func_call,
            Return_Node     : self.visit_return,
            Continue_Node   : self.visit_continue,
            Break_Node      : self.visit_break,
        }
        self.ast = ast
        self.path = []
        self.depth = 0

    @abstractmethod
    def visit_literal(self, node):
        pass

    @abstractmethod
    def visit_var(self, node):
        pass

    @abstractmethod
    def visit_type(self, node):
        pass

    @abstractmethod
    def visit_binop(self, node):
        pass

    @abstractmethod
    def visit_unop(self, node):
        pass

    @abstractmethod
    def visit_var_decl(self, node):
        pass

    @abstractmethod
    def visit_var_assign(self, node):
        pass

    @abstractmethod
    def visit_if_else(self, node):
        pass

    @abstractmethod
    def visit_loop(self, node):
        pass

    @abstractmethod
    def visit_func_decl(self, node):
        pass

    @abstractmethod
    def visit_func_call(self, node):
        pass

    @abstractmethod
    def visit_return(self, node):
        pass

    @abstractmethod
    def visit_continue(self, node):
        pass

    @abstractmethod
    def visit_break(self, node):
        pass

    @abstractmethod
    def visit_block(self, node):
        pass

    def visit_node(self, node):
        if not node:
            return

        self.path.append(node)
        
        self.depth += 1
        result = self.nodes_handlers[type(node)](node)
        self.depth -= 1
        return result

    def traverse(self):
        self.path.clear()
        self.visit_node(self.ast)