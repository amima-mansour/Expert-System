import sys

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def is_empty(self):
        return (self.items == [])

def eval_postfix(expr):
    print(expr)
    stack = Stack()
    for token in expr:
        if token == "+":
            result = stack.pop() and stack.pop()
            stack.push(result)
        elif token == "|":
            result = stack.pop() or stack.pop()
            stack.push(result)
        elif token == "^":
            a = stack.pop()
            b = stack.pop()
            result = (not(a) and b) or (a and not(b))
            stack.push(result)
        elif token == "!":
            result = not stack.pop()
            stack.push(result)
        else:
            stack.push(token)
    print(stack)
    return stack.pop()

def reverse_eval_postfix(result, value, op):
    if op == '|':
        if result == False:
            if value == True:
                print ("conflict")
                sys.exit(-1)
            return False
        if value == False:
            return (True)
        return ("Undetermined")
    if op == '+':
        if result == True:
            if value == False:
                print ("conflict")
                sys.exit(-1)
            return (True)
        if value == True:
            return (False)
        return ("Undetermined")