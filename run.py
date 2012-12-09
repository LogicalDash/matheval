import sys, os, re, math, string

class Operation:
    def add(x, y):
        return x + y
    def sub(x, y):
        return x - y
    def mult(x, y):
        return x * y
    def div(x, y):
        return x / y
    ops = {'+' : add, '-' : sub, '*' : mult, '/' : div}
# Stringly representations of an operator and all its operands, in order.
# Comes with methods for translating them to Python-type operators and constants.
    def __init__(self, operator, *args, **kwargs):
        self.operator = operator
        if kwargs.has_key('operators'):
            self.ops = kwargs['operators']
        if kwargs.has_key('operands'):
            self.operands = kwargs['operands']
        else:
            self.operands = args
    def op(self):
# Translate the operator into something python can do stuff with. Presumably a function.
           return Operation.ops[self.operator]
    def do(self):
# Perform the operation on the operands and return the result.
        return self.op()(*self.operands)
    def setleft(self, arg):
        # It's possible that one or both of my operands were blank at
        # time of creation. Fix this now.
        i = self.operands.index('')
        self.operands[i] = arg
    def setright(self, arg):
        r = self.operands.reverse()
        i = len(self.operands) - r.index(arg) - 1
        self.operands[i] = arg
class Expression:
    # Many operations, some of them operating on others.
    # The expression obeys some order of operations, but that only comes up when
    # adding new operations to the expression, without specifying any grouping.
    # Sublists represent operators of the same priority.
    # This list is from highest priority to lowest.
    order = ['*','/',['+','-']]
    def __init__(self, contents=None, order=None):
        if order is not None:
            self.order = order
        self.contents = []
        if type(contents) is list:
            i = 0
            for item in contents:
                if type(item) is str:
                    oper = ''
                    for ch in item:
                        if ch in self.ops():
                            oper = ch
                            break
                    argstr = item.remove(oper)
                    arg1 = ''
                    i = 0
                    # in case of leading spaces
                    while argstr[i] not in string.digits:
                        i += 1
                    while argstr[i] in string.digits:
                        arg1 += argstr[i]
                        i += 1
                    #in case of extra spaces in middle
                    while argstr[i] not in string.digits:
                        i += 1
                    arg2 = ''
                    while argstr[i] in string.digits:
                        arg2 += argstr[i]
                    self.contents.append(Operation(oper, arg1, arg2))
                elif type(item) is list:
                    self.contents.append(Expression(item, self.order))
                i += 1
    def order_lookup(self, op):
        if isinstance(op, Expression):
            return -1
        i = 0
        for item in self.order:
            if type(item) is list:
                if op in item:
                    return i
            elif item == op:
                return i
            i += 1
        return None
    def ops(self):
        r = []
        for item in self.order:
            if type(item) is list:
                for op in item:
                    r.append(op)
            else:
                r.append(item)
        return r
    def priorities(self):
        r = {}
        for op in self.ops():
            r[op] = self.order_lookup(op)
        return r
    def all_indices_of_operator(self, op):
        r = []
        i = 0
        for item in self.contents:
            if type(item) is list:
                if op in [operation.operator for operation in item]:
                    r.append(i)
            else:
                if item.operator is op:
                    r.append(i)
            i += 1
        return r
    def prioritize(self):
        # Return indices in the order they should be evaluated.
        # Expressions always get evaluated first--that's the
        # equivalent of putting them in parentheses.
        ex = []
        i = 0
        for item in self.contents:
            if isinstance(item, Expression):
                ex.append(i)
            i += 1
        i = 0
        while i < len(self.order):
            j = 0
            for item in self.contents:
                if self.order_lookup(item) == i:
                    ex.append(j)
                j += 1
            i += 1
    def cmpord(self, op1, op2):
        i1 = self.order_lookup(op1)
        i2 = self.order_lookup(op2)
        return i1 - i2
    def before(self, op1, op2):
        return self.cmpord(op1, op2) < 0
    def after(self, op1, op2):
        return self.cmpord(op1, op2) > 0
    def concurrent(self, op1, op2):
        return self.cmpord(op1, op2) == 0
    def fromstring(self, s):
        pass
    def add(self, op):
        self.contents.append(op)
    def remove(self, op):
        self.contents.remove(op)
    def insert(self, i, op):
        self.contents.insert(i, op)
    def append(self, op):
        self.contents.append(op)
    def count(self, val):
        return self.contents.count(val)
    def extend(self, it):
        self.contents.extend(it)
    def pop(self, i=-1):
        return self.contents.pop(i)
    def group(self, i):
        # Groups the operation at the given index with the one to its right.
        op1 = self.contents[i]
        op2 = self.contents[i+1]
        del self.contents[i+1]
        del self.contents[i]
        self.contents.insert(i, Expression(order=self.order,
                                           contents=[op1, op2]))

def parensplit(s):
    if type(s) is list:
        for item in list:
            if type(item) is str:
                if '(' in item:
                    item = parensplit(item)
        return s
    i = 0
    j = 0
    copying = False
    depth = 1
    parl = [""]
    news = ""
    while i < len(s):
        if not copying:
            if s[i] == '(':
                copying = True
            else:
                parl[j] += s[i]
        else:
            if s[i] == '(':
                news += s[i]
                depth += 1
            elif s[i] == ')':
                if depth > 1:
                    news += s[i]
                    depth -= 1
                else:
                    parl.append(news)
                    parl.append("")
                    j += 2
                    news = ""
                    copying = False
            else:
                news += s[i]
    return parl
                    
class Parser:
    def __init__(self, s, ops=['+','-','*','/']):
        self.s = s
        self.ops = ops
    def tolist(self):
        if hasattr(self, l):
            return self.l
        else:
            self.l = parensplit([self.s])
            return self.l
    def toex(self):
        if hasattr(self, ex):
            return self.ex
        if not hasattr(self, l):
            self.tolist()
        self.ex = Expression(self.l)
        return self.ex
    def calc(self):
        if hasattr(self, val):
            return self.val
        if not hasattr(self, ex):
            self.toex()
        self.val = self.ex.calc()
        return self.val
        
