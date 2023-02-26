from enum import Enum
from interpreter.ast import *
from interpreter.error import *
from interpreter.builtins import *
from interpreter.semantics import *


class EvaluationLoop(TreeVisitor):

    class BlockRetType(Enum):
        CONTINUE = 1,
        BREAK = 2,

    def __init__(self, ast: AST_Node, scope_controller: ScopeController):
        super().__init__(ast)
        self.silent = False
        self.scope_controller = scope_controller
        self.cur_block_node = None
    
        self.cur_func_symbol = None

    def get_scope(self):
        return self.scope_controller.get_scope(self.cur_block_node)

    def type_cast(self, type_name: str, value: any):
        conversion = {
            INT_TYPE.name   : int,
            FLOAT_TYPE.name : float,
            STR_TYPE.name   : str,
            BOOL_TYPE.name  : bool
        }
        return conversion[type_name](value)

    def visit_literal(self, node):
        conversion = {
            TokenType.INT_LITERAL   : int,
            TokenType.FLOAT_LITERAL : float,
            TokenType.STR_LITERAL   : str
        }
        return conversion[node.start_token.type](node.value)

    def visit_var(self, node):
        scope = self.get_scope()
        var_symbol = scope.get_symbol(node.name)
        return var_symbol.value

    def visit_type(self, node):
        pass

    def visit_binop(self, node):
        op = node.start_token.type
        left = self.visit_node(node.left)
        right = self.visit_node(node.right)

        operation = {
            TokenType.PLUS_OP  : lambda x, y: x + y,
            TokenType.MINUS_OP : lambda x, y: x - y,
            TokenType.MULT_OP  : lambda x, y: x * y,
            TokenType.DIV_OP   : lambda x, y: x / y,
            TokenType.AND_OP   : lambda x, y: x and y,
            TokenType.OR_OP    : lambda x, y: x or y,

            TokenType.GT_OP    : lambda x, y: x > y,
            TokenType.GTE_OP   : lambda x, y: x >= y,
            TokenType.LT_OP    : lambda x, y: x < y,
            TokenType.LTE_OP   : lambda x, y: x <= y,
            TokenType.EQ_OP    : lambda x, y: x == y,
            TokenType.NEQ_OP   : lambda x, y: x != y,
        }

        return operation[op](left, right)

    def visit_unop(self, node):
        op = node.start_token.type
        left = self.visit_node(node.left)

        operation = {
            TokenType.MINUS_OP : lambda x: -x,
            TokenType.NOT_OP   : lambda x: not x,
        }

        return operation[op](left)

    def visit_var_decl(self, node):
        scope = self.get_scope()
        var_symbol = scope.get_symbol(node.name)
        init_value = None
        if node.value:
            init_value = self.type_cast(
                var_symbol.type.name,
                self.visit_node(node.value)
            )
        var_symbol.value = init_value

    def visit_var_assign(self, node):
        scope = self.get_scope()
        var_symbol = scope.get_symbol(node.name)
        var_symbol.value = self.type_cast(
            var_symbol.type.name,
            self.visit_node(node.value)
        )

    def visit_if_else(self, node):
        cond_res = True
        if node.condition:
            cond_res = self.visit_node(node.condition)
        
        if cond_res:
            return self.visit_node(node.body)
        elif node.else_branch:
            return self.visit_node(node.else_branch)
        
    def visit_loop(self, node):
        # loop with condition
        if node.var:
            range_from_val = self.visit_node(node.range[0])
            range_to_val = self.visit_node(node.range[1])
            step = 0
            if node.step:
                step = self.visit_node(node.step)
            else:
                step = 1 if range_from_val < range_to_val else -1
            
            scope = None
            if isinstance(node.var, Var_Decl_Node):
                scope = self.scope_controller.get_scope(node.body)
            else:
                scope = self.get_scope()

            it_var_symbol = scope.get_symbol(node.var.name)

            # loop runtime logic
            it_var_symbol.value = range_from_val
            for it_var_symbol.value in range (range_from_val, range_to_val, step):
                result = self.visit_node(node.body)
                if result != None:
                    if result == self.BlockRetType.BREAK:
                        break
                    elif result == self.BlockRetType.CONTINUE:
                        continue
                    # return case
                    else:
                        return result
        # loop without condition
        else:
            while True:
                result = self.visit_node(node.body)
                if result != None:
                    if result == self.BlockRetType.BREAK:
                        break
                    elif result == self.BlockRetType.CONTINUE:
                        continue
                    # return case
                    else:
                        return result
        
        return None
    
    def visit_func_decl(self, node):
        func_body_scope = self.scope_controller.get_scope(node.body)
        func_symbol = func_body_scope.get_symbol(node.name)

        def func(*args):
            # setting current args and saving args values of previous func call
            prev_call_params = []
            for i in range(len(node.params)):
                param_symbol = func_body_scope.get_symbol(node.params[i].name)
                prev_call_params.append(param_symbol.value)
                param_symbol.value = args[i]

            # func body evaluation
            tmp_func_symbol = self.cur_func_symbol
            self.cur_func_symbol = func_symbol
            result = self.visit_node(node.body)
            self.cur_func_symbol = tmp_func_symbol

            # back to params of the previous func call
            for i in range(len(node.params)):
                param_symbol.value = prev_call_params.pop()

            return result
        
        func_symbol.value = func

    def visit_func_call(self, node):
        scope = self.get_scope()
        func_symbol = scope.get_symbol(node.name)
        func = func_symbol.value
        args = [self.visit_node(arg) for arg in node.args]
        return func(*args)

    def visit_return(self, node):
        assert self.cur_func_symbol
        ret_value = self.visit_node(node.value)
        return self.type_cast(self.cur_func_symbol.ret_type.name, ret_value)

    def visit_continue(self, node):
        return self.BlockRetType.CONTINUE

    def visit_break(self, node):
        return self.BlockRetType.BREAK

    def visit_block(self, node):
        prev_block_node = self.cur_block_node
        self.cur_block_node = node
        
        is_global_scope = self.get_scope() == self.scope_controller.get_global_scope()

        ret_value = None

        for stm in node.statements:
            stm_result = self.visit_node(stm)

            if stm_result != None and not is_global_scope:
                ret_value = stm_result
                break

        self.cur_block_node = prev_block_node

        return ret_value

    def evaluate(self):
        self.traverse()
