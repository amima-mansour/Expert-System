#!/usr/bin/Python3.4

import errors

def eval_postfix(expr):
    """Resolve an equation took in an RPN form.
        Takes the expr <list>"""

    stack = []
    for token in expr:
        if token == "+":
            a = stack.pop()
            b = stack.pop()
            result = a and b
            stack.append(result)
        elif token == "|":
            a = stack.pop()
            b = stack.pop()
            result = a or b
            stack.append(result)
        elif token == "^":
            a = stack.pop()
            b = stack.pop()
            result = (not(a) and b) or (a and not(b))
            stack.append(result)
        elif token == "!":
            result = not stack.pop()
            stack.append(result)
        else:
            stack.append(token)
    return stack.pop()

def reverse_eval_postfix(result, expr, c):
    """Trying to resolve equation where the unknown is not isolated
        by trying with both value and seeing if the result is coherent.
        If both value can match, return None as \'Undefined result\'.
        Takes the result <bool> of the equation, it's expr <list>,
        and the c <char> we're looking for."""

    # print("expr = {}".format(expr))
    expr2 = list(expr)
    expr[expr.index(c)] = True
    value1 = eval_postfix(expr)
    expr2[expr2.index(c)] = False
    value2 = eval_postfix(expr2)
    if value1 == value2:
        return None
    if value1 == result:
        return True
    return False

if __name__ == '__main__':
    from sys import argv as av

    if len(av) == 3 and av[1] == "-r":
        expr = list(av[2])
        print(reverse_infix(expr))
    elif len(av) > 1:
        expr = []
        for arg in av[1:]:
            if arg == 'T':
                expr.append(True)
            elif arg == 'F':
                expr.append(False)
            else:
                expr.append(arg)
        print("For input {}".format(expr))
        print("eval_postfix = {}".format(eval_postfix(expr)))
