
class BuiltinType():
    def __init__(self, name: str):
        self.name = name

INT_TYPE   = BuiltinType("int")
FLOAT_TYPE = BuiltinType("float")
STR_TYPE   = BuiltinType("str")
BOOL_TYPE  = BuiltinType("bool")
ANY_TYPE   = BuiltinType("any")