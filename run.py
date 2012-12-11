import sys, os, re, math, string, copy

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
    def __init__(self, s):
        for op in self.ops.keys():
            if op in s:
                self.operator = op
                break
        self.operands = [ argh.strip() for argh in s.split(self.operator) ]
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.operator != other.operator:
            return False
        if len(self.operands) != len(other.operands):
            return False
        i = 0
        while i<len(self.operands):
            if self.operands[i] != other.operands[i]:
                return False
            i += 1
        return True
    def fill_with(self, left, right):
        if self.operands[0] == '' and left is not None:
            self.operands[0] = left
        if self.operands[-1] == '' and right is not None:
            self.operands[-1] = right
    def op(self):
        # Translate the operator into something python can do stuff with. Presumably a function.
        return Operation.ops[self.operator]
    def iconv(self):
        # Convert the stringy arguments into integers.
        r = []
        for operand in self.operands:
            if type(operand) is type(0):
                r.append(operand)
            elif type(operand) is type(""):
                r.append(int(operand))
            else:
                print "What's %s doing here?" % operand
        return r
    def do(self):
        # Perform the operation on the operands and return the result.
        print "Performing operation %s on %s" % (self.op(), repr(self.operands))
        print "It will give result %d" % self.op()(*self.iconv())
        return self.op()(*self.iconv())
    def __repr__(self):
        return "(" + repr(self.operands) + ", " + self.operator + ")"
class Expression:
    # Many operations, some of them operating on others.
    # The expression obeys some order of operations.
    # Sublists within order represent operators of the same priority.
    # order is ordered from highest priority to lowest.
    def __init__(self, contents=[], order=['*','/',['+','-']]):
        self.order = order
        self.getops()
        self.contents = []
        if type(contents) is not type([]):
            contents = [contents]
        for item in contents:
            if type(item) is str:
                mitey = item.replace(" ","")
                print "Converting a string, %s, to Operation for use in an Expression" % mitey
                for oppa in self.ops:
                    while True:
                        try:
                            style = mitey.index(oppa)
                        except:
                            break
                        leftbound = style-1
                        while leftbound >= 0 and mitey[leftbound] in string.digits:
                            leftbound -= 1
                        if leftbound < 0 or mitey[leftbound] not in string.digits:
                            leftbound += 1
                        rightbound = style+1
                        while rightbound < len(mitey) and mitey[rightbound] in string.digits:
                            rightbound += 1
                        self.contents.append(Operation(mitey[leftbound:rightbound]))
                        mitey = mitey[:leftbound] + mitey[rightbound:]
            elif type(item) is list and len(item) > 0:
                print "Converting a list, %s, to an Expression, for use in another Expression" % item
                self.contents.append(Expression(item, self.order))
            elif isinstance(item, Operation):
                print "Adding a premade Operation, %s, to an Expression" % item
                self.contents.append(item)
    def __eq__(self, other):
        if len(self.contents) != len(other.contents):
            return False
        i = 0
        while i < len(self.contents):
            if self.contents[i] != other.contents[i]:
                return False
            i += 1
        return True
    def order_lookup(self, op):
        if isinstance(op, Expression):
            return -1
        if isinstance(op, Operation):
            op = op.operator
        i = 0
        for item in self.order:
            if type(item) is list:
                for thing in item:
                    if thing == op:
                        return i
            elif item == op:
                return i
            i += 1

    def getops(self):
        r = []
        for item in self.order:
            if type(item) is list:
                for op in item:
                    r.append(op)
            else:
                r.append(item)
        self.ops = r
    def priorities(self):
        r = {}
        for op in self.ops():
            r[op] = self.order_lookup(op)
        return r
    def prioritize(self):
        # Return indices in the order they should be evaluated.
        # Expressions always get evaluated first--that's the
        # equivalent of putting them in parentheses.
        ex = []
        # Expressions go first
        i = 0
        while i < len(self.contents):
            if isinstance(self.contents[i], Expression):
                ex.append(i)
            i += 1
        # Filled-in opers go next
        for level in self.order:
            if type(level) is type([]):
                classist = ''.join(level)
            else:
                classist = level
            i = 0
            for oppo in self.contents:
                if isinstance(oppo, Operation) and not '' in oppo.operands:
                    ex.append(i)
                i += 1
        # Half-filled next
        for level in self.order:
            if type(level) is type([]):
                classist = ''.join(level)
            else:
                classist = level
            i = 0
            for oppo in self.contents:
                if isinstance(oppo, Operation) and oppo.operands.count('') == 1:
                    ex.append(i)
                i += 1
        # Unfilled last
        for level in self.order:
            if type(level) is type([]):
                classist = ''.join(level)
            else:
                classist = level
            i = 0
            for oppo in self.contents:
                if isinstance(oppo, Operation) and oppo.operands.count('') > 1:
                    ex.append(i)
                i += 1
        return ex
    def calc(self):
        agenda = self.prioritize()
        working = copy.deepcopy(self.contents)
        for i in agenda:
            work = copy.deepcopy(self.contents[i])
            print "working on %s" % repr(work)
            wi = 0
            while wi < len(working):
                if work == working[wi]:
                    break
                wi += 1
            if wi == len(working):
                print "%s was not found in %s" % (work, working)
                continue
            if type(work) is type(0):
                continue
            elif isinstance(work, Expression):
                done = work.calc()
                working[wi] = done
            elif isinstance(work, Operation): # it's an operation
                # Fill in missing arguments with what's already been done.
                # I'm assuming I got the agenda right, and therefore there are enough numbers in the right places.
                if i + 1 < len(working) and type(working[i+1]) in [type(''), type(0)]:
                    right = working[i+1]
                    del working[i+1]
                else:
                    right = None
                if i - 1 >= 0 and type(working[i-1]) in [type(''), type(0)]:
                    left = working[i-1]
                    del working[i-1]
                else:
                    left = None
                work.fill_with(left, right)
                done = work.do()
                working[wi] = done
            else:
                print "What am I supposed to do with this?"
                print work
                exit(1)
        # If I got all that right, working should gradually shrink as
        # the operations and expressions are replaced with numbers
        # that go into other operations. The degenerate case of that
        # is a list with one number in it.
        return str(working)
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

def par2subl(s):
    r = [""]
    depth = 0
    parenno = 0
    for ch in s:
        if depth == 0:
            if ch == "(":
                depth = 1
                parenno += 1
                r.append("")
            else:
                r[parenno] += ch
        else:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    r.append("")
                    parenno += 1
            else:
                r[parenno] += ch
    return r

def parensplit(x):
    if type(x) is type(""):
        if "(" in x:
            return parensplit(par2subl(x))
        else:
            return x
    elif type(x) is type([]):
        return [ z for z in [ parensplit(y) for y in x ] if z is not None ]
    else:
        return None

class Parser:
    def __init__(self, s):
        self.s = s
    def tolist(self):
        if hasattr(self, 'l'):
            return self.l
        else:
            print "I'm makin' a list out of %s" % self.s
            self.l = parensplit(self.s)
            print repr(self.l)
            return self.l
    def toex(self):
        if hasattr(self, 'ex'):
            return self.ex
        if not hasattr(self, 'l'):
            self.tolist()
        print "I'm makin' an expression out of %s" % repr(self.l)
        self.ex = Expression(self.l)
        return self.ex
    def calc(self):
        if hasattr(self, 'val'):
            return self.val
        if not hasattr(self, 'ex'):
            self.toex()
        return self.ex.calc()
        
equation = " ".join(sys.argv[1:])
pars = Parser(equation)
print pars.calc()
