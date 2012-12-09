import sys, os, re, math

class Operation:
    ops = {'+' : lambda x y : x + y, '-' : lambda x y : x - y,
           '*' : lambda x y : x * y, '/' : lambda x y : x / y}
# Stringly representations of an operator and all its operands, in order.
# Comes with methods for translating them to Python-type operators and constants.
    def __init__(self, operator, *operands):
        self.operator = operator
        self.operands = operands
    def op(self):
# Translate the operator into something python can do stuff with. Presumably a function.
           return Operation.ops[self.operator]
    def do(self):
# Perform the operation on the operands and return the result.
        return self.op()(*self.operands)
