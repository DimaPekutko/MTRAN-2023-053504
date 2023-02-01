from interpreter.ast import *
from interpreter.lexer import TokenType
from interpreter.error import syntax_error
from interpreter.ast import ast_printer

class Parser():
    """ Parses syntax tree from tokens """

    def __init__(self, tokens):
        self.tokens = tokens
    
    def remove_spaces(self):
        assert len(self.tokens)
        while self.tokens[0].type == TokenType.SPACE:
            self.tokens.pop(0) 

    def eat(self, token_types: list[TokenType] = []):
        assert len(self.tokens)

        if not TokenType.SPACE in token_types:
            self.remove_spaces() 

        token = self.tokens.pop(0)
        if token_types and not token.type in token_types:
            syntax_error(
                f"Unexpected token of type '{token.type}' found, but expected {token_types}", 
                token.value, 
                token.pos.row, token.pos.col, token.pos.filename
            )
        
        return token

    def peek(self, idx: int = 0):
        assert len(self.tokens) > idx
        return self.tokens[idx]

    def parse_expr(self):
        left = self.parse_comparison()
        op_token = self.peek()
        while (op_token.type in [TokenType.AND_OP, TokenType.OR_OP]):
            self.eat()
            left = Binary_Op_Node(op_token, left, self.parse_comparison(), op_token.type)
            op_token = self.peek()        

        return left

    def parse_comparison(self):
        left = self.parse_arithmetic_expr()
        op_token = self.peek()
        while (op_token.type in [
            TokenType.GT_OP, TokenType.GTE_OP, TokenType.LT_OP, 
            TokenType.LTE_OP, TokenType.EQ_OP, TokenType.NEQ_OP
        ]):
            self.eat()
            left = Binary_Op_Node(op_token, left, self.parse_arithmetic_expr(), op_token.type)
            op_token = self.peek()        

        return left

    def parse_arithmetic_expr(self):
        left = self.parse_term()
        op_token = self.peek()
        while (op_token.type in [TokenType.PLUS_OP, TokenType.MINUS_OP]):
            self.eat()
            left = Binary_Op_Node(op_token, left, self.parse_term(), op_token.type)
            op_token = self.peek()        

        return left

    def parse_term(self):
        left = self.parse_factor()
        op_token = self.peek()
        while (op_token.type in [TokenType.MULT_OP, TokenType.DIV_OP]):
            self.eat()
            left = Binary_Op_Node(op_token, left, self.parse_factor(), op_token.type)
            op_token = self.peek()        

        return left

    def parse_factor(self):
        token = self.peek()
        # found: literal
        if token.type in [TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL, TokenType.STR_LITERAL]:
            self.eat()
            return Literal_Node(token, token.value)
        # found : variable
        elif token.type == TokenType.IDENTIFIER:
            return self.parse_var()
        # found: (expr|factor|term)
        elif token.type == TokenType.LEFT_PAR:
            self.eat([TokenType.LEFT_PAR])
            node = self.parse_expr()
            self.eat([TokenType.RIGHT_PAR])
            return node
        # found: unop
        elif token.type in (TokenType.MINUS_OP, TokenType.NOT_OP):
            self.eat()
            return Unary_Op_Node(token, self.parse_factor(), token.type)
        # found: funccall
        elif token.type == TokenType.LEFT_BRACKET:
            return self.parse_func_call()

        else:
            syntax_error(
                f"Expected value, but received '{token.type}' token", 
                token.value, 
                token.pos.row, token.pos.col, token.pos.filename
            )

    def parse_var(self):
        token = self.eat([TokenType.IDENTIFIER])
        return Var_Node(token, token.value)

    def parse_type(self):
        token = self.eat([TokenType.IDENTIFIER])
        return Type_Node(token, token.value)

    def parse_var_decl(self, parse_with_init_value: bool = True):
        id_token = self.eat([TokenType.IDENTIFIER])
        type_node = self.parse_type()
        init_value = None
        if parse_with_init_value and self.peek().type == TokenType.ASSIGN_OP:
            self.eat([TokenType.ASSIGN_OP])
            init_value = self.parse_expr()
        return Var_Decl_Node(id_token, id_token.value, type_node, init_value)

    def parse_var_assign(self):
        id_token = self.eat([TokenType.IDENTIFIER])
        self.eat([TokenType.ASSIGN_OP])
        return Var_Assign_Node(id_token, id_token.value, self.parse_expr())

    def parse_if_else(self):
        token = self.eat()
        start_token = token

        condition = None # for ELSE_KWD condition will be None
        body = None
        else_branch = None

        if token.type in [TokenType.IF_KWD, TokenType.IFELSE_KWD]:
            condition = self.parse_expr()

        token = self.peek()
        
        if token.type == TokenType.LEFT_BRACE:
            body = self.parse_block()
        else:
            body = Block_Node(token, [ self.parse_statement() ])
        
        token = self.peek()
        if start_token.type != TokenType.ELSE_KWD:
            if token.type in [TokenType.IFELSE_KWD, TokenType.ELSE_KWD]:
                else_branch = self.parse_if_else()
        
        return If_Else_Node(start_token, condition, body, else_branch)

    def parse_loop(self):
        self.eat([TokenType.LOOP_KWD])

        token = self.peek(0)
        next_token = self.peek(1)
        start_token = token

        var = None
        loop_range = None
        step = None 
        body = None

        # var
        if (token.type == TokenType.IDENTIFIER):
            # var
            if next_token.type == TokenType.COMMA:
                var = self.parse_var()
            # var declaration
            elif next_token.type == TokenType.IDENTIFIER:
                var = self.parse_var_decl()
            else:
                syntax_error(
                    f"Expect var or var declaration, but token type '{next_token.type}' found",
                    next_token.value,
                    next_token.pos.row, next_token.pos.col, next_token.pos.filename)

            self.eat([TokenType.COMMA])
            # range
            start = self.parse_expr()
            self.eat([TokenType.RANGE_MARK])
            end = self.parse_expr()
            loop_range = (start, end)
            # step
            token = self.peek()
            if (token.type == TokenType.COMMA):
                self.eat()
                step = self.parse_expr()
        
        # print(self.peek().type)
        body = self.parse_block()
        return Loop_Node(start_token, var, loop_range, step, body)

    def parse_func_decl(self):
        token = self.eat([TokenType.DEF_KWD])
        start_token = token
        
        name = None
        params = []
        ret_type = None
        body = None

        # name
        token = self.eat([TokenType.IDENTIFIER])
        name = token.value
        # params
        self.eat([TokenType.PIPE])
        while self.peek().type != TokenType.PIPE:
            if len(params):
                self.eat([TokenType.COMMA])
            params.append(self.parse_var_decl(False))
        self.eat([TokenType.PIPE])
        # ret type
        self.eat([TokenType.RET_TYPE_MARK])
        ret_type = self.parse_type()
        # body
        body = self.parse_block()

        return Func_Decl_Node(start_token, name, params, ret_type, body)

    def parse_func_call(self):
        token = self.eat([TokenType.LEFT_BRACKET])
        start_token = token

        name = None
        args = []

        # name
        token = self.eat([TokenType.IDENTIFIER])
        name = token.value
        # args
        while self.peek().type != TokenType.RIGHT_BRACKET:
            if len(args):
                self.eat([TokenType.COMMA])
            args.append(self.parse_expr())

        self.eat([TokenType.RIGHT_BRACKET])

        return Func_Call_Node(start_token, name, args)

    def parse_return(self):
        token = self.eat([TokenType.EXCL_MARK])
        return Return_Node(token, self.parse_expr())        

    def parse_continue(self):
        token = self.eat([TokenType.NEXT_KWD])
        return Continue_Node(token)

    def parse_break(self):
        token = self.eat([TokenType.STOP_KWD])
        return Break_Node(token)

    def parse_block(self, require_braces: bool = True):
        token = self.peek()
        block = Block_Node(token, [])

        if require_braces:
            self.eat([TokenType.LEFT_BRACE])
            token = self.peek()

        while(not token.type in [TokenType.RIGHT_BRACE, TokenType.EOF]):
            next_token = self.peek(1)

            node = self.parse_statement()

            block.statements.append(node)
            token = self.peek()

        if require_braces:
            self.eat([TokenType.RIGHT_BRACE])

        return block

    def parse_statement(self):
        node = None
        token = self.peek(0)
        next_token = self.peek(1)

        if token.type == TokenType.IDENTIFIER:
            # var decl
            if next_token.type == TokenType.IDENTIFIER:
                node = self.parse_var_decl()
            # var assign
            elif next_token.type == TokenType.ASSIGN_OP:
                node = self.parse_var_assign()

        # if else chain
        elif token.type == TokenType.IF_KWD:
            node = self.parse_if_else()

        # cycle statement
        elif token.type == TokenType.LOOP_KWD:
            node = self.parse_loop()
        
        # func declaration
        elif token.type == TokenType.DEF_KWD:
            node = self.parse_func_decl()
        
        # func call
        elif token.type == TokenType.LEFT_BRACKET:
            node = self.parse_func_call()

        # func return
        elif token.type == TokenType.EXCL_MARK:
            node = self.parse_return();

        elif token.type == TokenType.NEXT_KWD:
            node = self.parse_continue()
        
        elif token.type == TokenType.STOP_KWD:
            node = self.parse_break()

        if not node or not isinstance(node, Statement_Node):
            syntax_error(
                f"Expect statement, but token type '{token.type}' found",
                token.value,
                token.pos.row, token.pos.col, token.pos.filename
            )

        if node.require_semicolon:
            self.eat([TokenType.SEMICOLON])
        
        return node

    def parse(self):
        """ Returns ast which is generated from tokens given to __init__ """
        
        self.tokens = list(filter(
            lambda token: not token.type in [TokenType.SPACE, TokenType.LINE_COMMENT], 
            self.tokens
        ))
        return self.parse_block(False)