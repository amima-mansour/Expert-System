#!/usr/bin/Python3.4

import errors

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
    stack = Stack()
    for token in expr:
        if token == "+":
            a = stack.pop()
            b = stack.pop()
            result = a and b
            stack.push(result)
        elif token == "|":
            a = stack.pop()
            b = stack.pop()
            result = a or b
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
    return stack.pop()

def reverse_eval_postfix(result, expr, c):
    print("expr = {}".format(expr))
    expr[expr.index(c)] = True
    value = eval_postfix(expr)
    if value == result:
        return True
    return False
