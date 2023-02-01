from abc import ABC
from interpreter.ast import *
from interpreter.builtins import *


class Symbol(ABC):
    def __init__(self, name: str):
        self.value = None
        self.name = name
        # will be set and used during evaluation
        # or in case this symbol is builtin
        self.value = None


class Symbol_Type(Symbol):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name


class Symbol_Var(Symbol):
    def __init__(self, name: str, type_symbol: Symbol_Type):
        super().__init__(name)
        self.type = type_symbol


class Symbol_Func(Symbol):
    def __init__(self, name: str, params_types: list[Symbol_Type], ret_type_symbol: Symbol_Type):
        super().__init__(name)
        self.params_types = params_types
        self.ret_type = ret_type_symbol


class SymbolTable():
    def __init__(self, block_node, parent_scope = None, initial_symbols = {}):
        self.block_node = block_node
        self.parent_scope = parent_scope
        # str : Symbol
        self.__symbols = initial_symbols

    def __repr__(self):
        res_str = ""
        for name, symbol in self.__symbols.items():
            res_str += f"\n{name} -> {type(symbol).__name__}"
        return res_str

    def get_symbol(self, name: str):
        symbol = self.__symbols.get(name)

        if symbol == None and self.parent_scope:
            symbol = self.parent_scope.get_symbol(name)

        return symbol

    def add_symbol(self, name: str, symbol: Symbol):
        self.__symbols[name] = symbol


class ScopeController():
    def __init__(self, program_node: AST_Node):
        self.__global_scope = SymbolTable(
            program_node, 
            initial_symbols = self.get_initial_global_symbols()
        )
        # block_node : SymbolTable
        self.__scopes = {
            program_node: self.__global_scope
        }
    
    def get_initial_global_symbols(self):
        """ Creates globals symbols dict from builtins """

        global_symbols = {
            INT_TYPE.name   : Symbol_Type(INT_TYPE.name),
            FLOAT_TYPE.name : Symbol_Type(FLOAT_TYPE.name),
            STR_TYPE.name   : Symbol_Type(STR_TYPE.name),
            BOOL_TYPE.name  : Symbol_Type(BOOL_TYPE.name),
            ANY_TYPE.name   : Symbol_Type(ANY_TYPE.name)
        }

        # intrinsics
        for intr in INTRINSICS_LIST:
            # vars
            if type(intr) == IntrinsicVar:
                global_symbols[intr.name] = Symbol_Var(intr.name, global_symbols[intr.type.name])
            # funcs
            elif type(intr) == IntrinsicFunc:
                params_types = []
                for arg_type in intr.args_types:
                    params_types.append(global_symbols[arg_type.name])
                global_symbols[intr.name] = Symbol_Func(intr.name, params_types, global_symbols[intr.type.name])

            global_symbols[intr.name].value = intr.actual_value;

        return global_symbols

    def __repr__(self):
        res_str = ""
        for block_node, scope in self.__scopes.items():
            res_str += scope.__repr__() + "\n"
        return res_str

    def new_scope(self, block_node: AST_Node, parent_scope: SymbolTable):
        table = SymbolTable(block_node, parent_scope=parent_scope, initial_symbols={})
        self.__scopes[block_node] = table
        return table

    def get_global_scope(self):
        return self.__global_scope
    
    def get_scope(self, node):
        return self.__scopes.get(node)