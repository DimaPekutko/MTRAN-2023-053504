from interpreter.ast import *
from interpreter.error import semantic_error
from interpreter.lexer import TokenType
from interpreter.builtins import *
from .scopes import *


class SemanticAnalyzer(TreeVisitor):
    """ Analyzes AST with specific semantic rules and 
        also generates chain of symbol scopes related to AST block nodes """

    def __init__(self, ast):
        super().__init__(ast)
        self.scope_controller = ScopeController(ast)
        self.scope = None

        # lazy method to check contrinue, break, return statements semantics
        self.loop_block_now = False
        self.current_func_symbol = None

        # needs to add vars in scopes properly
        self.add_vardecl_to_scope = True 

    def type_check(self, node, left_type, right_type, err_code_fragment):
        if left_type != right_type:
            semantic_error(
                f"Cannot cast '{right_type.name}' type expr to '{left_type.name}' type", 
                err_code_fragment, node.start_token.pos.row, node.start_token.pos.col, 
                node.start_token.pos.filename
            )

    def visit_literal(self, node):
        token_type = node.start_token.type

        type_binding = {
            TokenType.INT_LITERAL   : INT_TYPE.name,
            TokenType.FLOAT_LITERAL : FLOAT_TYPE.name,
            TokenType.STR_LITERAL   : STR_TYPE.name
        }

        # assert 0 & "Should not be here"
        return self.scope.get_symbol(type_binding[node.start_token.type])
        

    def visit_var(self, node):
        var_symbol = self.scope.get_symbol(node.name)
        if not isinstance(var_symbol, Symbol_Var):
            semantic_error(
                f"Cannot find var '{node.name}'", node.name, 
                node.start_token.pos.row, node.start_token.pos.col, node.start_token.pos.filename
            )

        return var_symbol.type 

    def visit_type(self, node):
        type_symbol = self.scope.get_symbol(node.name)
        if not isinstance(type_symbol, Symbol_Type):
            semantic_error(
                f"Can not find type '{node.name}'", node.name, 
                node.start_token.pos.row, node.start_token.pos.col, node.start_token.pos.filename
            )
        return self.scope.get_symbol(node.name)

    def visit_binop(self, node):
        left_type = self.visit_node(node.left)
        right_type = self.visit_node(node.right)
        
        op = node.start_token.type

        int_type = self.scope.get_symbol(INT_TYPE.name)
        float_type = self.scope.get_symbol(FLOAT_TYPE.name)
        bool_type = self.scope.get_symbol(BOOL_TYPE.name)

        ret_type = {
            TokenType.PLUS_OP  : left_type,
            TokenType.MINUS_OP : left_type,
            TokenType.MULT_OP  : left_type,
            TokenType.DIV_OP   : left_type,
            TokenType.AND_OP   : bool_type,
            TokenType.OR_OP    : bool_type,
            TokenType.GT_OP    : bool_type,
            TokenType.GTE_OP   : bool_type,
            TokenType.LT_OP    : bool_type,
            TokenType.LTE_OP   : bool_type,
            TokenType.EQ_OP    : bool_type,
            TokenType.NEQ_OP   : bool_type,
        }

        self.type_check(node, left_type, right_type, node.start_token.value)
        return ret_type[op]

    def visit_unop(self, node):
        left_type =  self.visit_node(node.left)
        op = node.start_token.type

        bool_type = self.scope.get_symbol(BOOL_TYPE.name)
        ret_type = {
            TokenType.NOT_OP   : bool_type,
            TokenType.MINUS_OP : left_type,
        }

        return ret_type[op]

    def visit_var_decl(self, node):
        type_symbol = self.visit_node(node.type_node)
        var_symbol = Symbol_Var(node.name, type_symbol)

        if node.value:
            rhs_type_symbol = self.visit_node(node.value)
            self.type_check(node, type_symbol, rhs_type_symbol, node.name)
        
        if self.add_vardecl_to_scope:
            self.scope.add_symbol(node.name, var_symbol)

        return var_symbol

    def visit_var_assign(self, node):
        var_symbol = self.scope.get_symbol(node.name)
        if not isinstance(var_symbol, Symbol_Var):
            semantic_error(
                f"Can not find var '{node.name}'", node.name, 
                node.start_token.pos.row, node.start_token.pos.col, node.start_token.pos.filename
            )
        
        self.type_check(node, var_symbol.type, self.visit_node(node.value), node.name)

        return var_symbol.type 

    def visit_if_else(self, node):
        if node.condition:
            self.visit_node(node.condition)

        self.visit_node(node.body)

        if node.else_branch:
            self.visit_node(node.else_branch)
        
    def visit_loop(self, node):
        tmp_loop_now = self.loop_block_now

        if node.var:
            # Setting iteration var at the begining of the loop block.
            # It's need to add var symbol in scope properly.
            node.body.statements.insert(0, node.var)
            self.loop_block_now = True
            loop_scope = self.visit_node(node.body)
            self.loop_block_now = tmp_loop_now
            node.body.statements.pop(0)            

            var_type = loop_scope.get_symbol(node.var.name).type

            if node.range:
                start_val_type = self.visit_node(node.range[0])
                end_val_type = self.visit_node(node.range[1])

                self.type_check(node, var_type, start_val_type, node.start_token.value)
                self.type_check(node, var_type, end_val_type, node.start_token.value)

            if node.step:
                step_type = self.visit_node(node.step)
            
                self.type_check(node, var_type, step_type, node.start_token.value)

        else:
            self.loop_block_now = True
            self.visit_node(node.body)
            self.loop_block_now = tmp_loop_now
    
    def visit_func_decl(self, node):
        type_symbol = self.visit_node(node.ret_type_node)

        func_symbol = Symbol_Func(node.name, [], type_symbol)
        self.scope.add_symbol(node.name, func_symbol)

        # Setting params as var decl statements 
        # at the begining of the function block.
        # It's need to add params in symbol scope properly.
        self.add_vardecl_to_scope = False
        for param in node.params:
            assert param
            func_symbol.params_types.append(self.visit_node(param).type)
            node.body.statements.insert(0, param)
        self.add_vardecl_to_scope = True

        tmp_current_func_symbol = self.current_func_symbol
        self.current_func_symbol = func_symbol
        func_scope = self.visit_node(node.body)
        self.current_func_symbol = tmp_current_func_symbol
        
        # Setting back actual statements in body  
        for param in node.params:
            node.body.statements.pop(0)
        

    def visit_func_call(self, node):
        func_symbol = self.scope.get_symbol(node.name)
        if not isinstance(func_symbol, Symbol_Func):
            semantic_error(
                f"Cannot find func '{node.name}'", node.name, 
                node.start_token.pos.row, node.start_token.pos.col, node.start_token.pos.filename
            )
        
        # matching func call args to func params
        if len(func_symbol.params_types) != len(node.args):
            semantic_error(
                f"Arguments count of func call '{node.name}' does not match count of function params", node.name, 
                node.start_token.pos.row, node.start_token.pos.col, node.start_token.pos.filename
            )
        for i in range(len(func_symbol.params_types)):
            param_type = func_symbol.params_types[i]
            arg_type = self.visit_node(node.args[i])
            self.type_check(node.args[i], param_type, arg_type, node.args[i].start_token.value)
        
        return func_symbol.ret_type

    def visit_return(self, node):
        if not self.current_func_symbol:
            semantic_error(
                f"Unexpected '{node.start_token.value}' statemnt found outside a function", node.start_token.value, 
                node.start_token.pos.row, node.start_token.pos.col, node.start_token.pos.filename
            )        

        self.type_check(node, self.current_func_symbol.ret_type, self.visit_node(node.value), node.start_token.value)

    def visit_continue(self, node):
        if not self.loop_block_now:
            semantic_error(
                f"Unexpected '{node.start_token.value}' statemnt found outside a loop", node.start_token.value, 
                node.start_token.pos.row, node.start_token.pos.col, node.start_token.pos.filename
            )

    def visit_break(self, node):
        if not self.loop_block_now:
            semantic_error(
                f"Unexpected '{node.start_token.value}' statemnt found outside a loop", node.start_token.value, 
                node.start_token.pos.row, node.start_token.pos.col, node.start_token.pos.filename
            )

    def visit_block(self, node):
        if not self.scope:
            self.scope = self.scope_controller.get_global_scope()
        else:
            self.scope = self.scope_controller.new_scope(node, self.scope)

        for stm in node.statements:
            self.visit_node(stm)
        
        tmp_scope = self.scope

        self.scope = self.scope.parent_scope
        
        return tmp_scope

    def analyze(self):
        self.traverse()
        return self.scope_controller
        # self.__print(f"Block")
        # for stm in node.statements:
        #     self.visit_node(stm)