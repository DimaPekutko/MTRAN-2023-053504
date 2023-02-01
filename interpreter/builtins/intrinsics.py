from abc import ABC
from .types import *
from .definitions import *

class Intrinsic(ABC):
    def __init__(self, name: str, intr_type: BuiltinType, actual_value: any):
        self.name = name
        self.type = intr_type
        self.actual_value = actual_value


class IntrinsicVar(Intrinsic):
    def __init__(self, name: str, intr_type: BuiltinType, actual_value: any):
        super().__init__(name, intr_type, actual_value)


class IntrinsicFunc(Intrinsic):
    def __init__(self, name: str, intr_type: BuiltinType, args_types: list[BuiltinType], actual_value: any):
        super().__init__(name, intr_type, actual_value)
        self.args_types = args_types


INTRINSICS_LIST = [
    IntrinsicVar("true",  BOOL_TYPE, True),
    IntrinsicVar("false", BOOL_TYPE, False),

    IntrinsicFunc("float_to_str", STR_TYPE, [FLOAT_TYPE], str),
    IntrinsicFunc("int_to_str", STR_TYPE, [INT_TYPE], str),
    IntrinsicFunc("bool_to_str", STR_TYPE, [BOOL_TYPE], str),
    
    IntrinsicFunc("str_to_int", INT_TYPE, [STR_TYPE], int),
    IntrinsicFunc("str_to_float", FLOAT_TYPE, [STR_TYPE], float),
    IntrinsicFunc("str_to_bool", BOOL_TYPE, [STR_TYPE], bool),
    
    IntrinsicFunc("show", ANY_TYPE, [STR_TYPE], lambda x : print(x, end="")),
    IntrinsicFunc("shown", ANY_TYPE, [STR_TYPE], print),
    IntrinsicFunc("read", STR_TYPE, [STR_TYPE], input),
    
]