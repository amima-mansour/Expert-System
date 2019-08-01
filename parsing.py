#!/usr/bin/Python3.4

import errors
import RPN as rpn
import beautiful_print as bp

user_input = False

def get_input():
    bp.print_title("Please enter your input : ")
    line = ""
    content = ""
    while not line.startswith('?'):
        try:
            line = input()
        except:
            errors.stoped_input()
        content += line + '\n'
    return content

def valid_arg(arg):
    if (len(arg) != 2 and len(arg) != 3) or arg[0] != '-':
        return False
    if arg[1:] != 'd' and arg[1:] != 'i' and arg[1:] != "di" and arg[1:] != "id":
        errors.usage()
    return True

def file_opener(name):
    'Try to open the file, takes it\'s name and return it\'s content as a string'

    if name is None:
        return None
    try:
        f = open(name, "r")
    except:
        errors.file_fail(name, "failed to open")
        return None
    if f.mode == "r":
        content = f.read()
        return content
    else:
        errors.file_fail(name, "couldn't read")

def is_upper(c):
    'Check if a string / character is upper alphabetical value'
    
    if type(c) is chr:
        ascii_val = ord(c)
        if ascii_val < 65 or ascii_val > 90:
            return False
        return True
    else:
        for e in c:
            ascii_val = ord(e)
            if ascii_val < 65 or ascii_val > 90:
                return False
        return True

def brackets(s):
    'The function below checks if parentheses are correctly closed'

    stack = []
    pushChar = '('
    popChar = ')'
    for c in s:
        if c == pushChar:
            stack.append(c)
        elif c == popChar:
            if stack == []:
                return False
            else:
                stack.pop()
    return stack == []

def rule_is_valid(line):
    'Check if a rule is given a valid way'

    ops = {
            '!': [['(', '+', '|', '^', 'S'], ['(', 'L']],
            '^': [[')', 'L'], ['(', 'L', '!']],
            '+': [[')', 'L'], ['(', 'L', '!']],
            '|': [[')', 'L'], ['(', 'L', '!']],
            '(': [['(', '!', '+', '|', '^', 'S'], ['(', 'L']],
            ')': [['L'], ['+', '|', '^', 'E', '<']],
            'L': [['(', '+', '|', '^', 'S', '!'], [')', '+', '|', '^', 'E', '<']],
            }
    split = line.split("=>")
    if len(split) != 2:
        return False
    for part in split:
        if not brackets(part):
            return False
        i = 0
        l = len(part)
        if l < 1:
            return False
        while i < l:
            if is_upper(part[i]):
                if (i > 0):
                    if is_upper(part[i - 1]) or part[i - 1] not in ops['L'][0]:
                        return False
                if (i + 1 < l):
                    if is_upper(part[i + 1]) or part[i + 1] not in ops['L'][1]:
                        return False
            elif part[i] in ops:
                if i == 0:
                    if 'S' not in ops[part[i]][0]:
                        return False
                elif is_upper(part[i - 1]):
                    if 'L' not in ops[part[i]][0]:
                        return False
                elif part[i - 1] not in ops[part[i]][0]:
                    return False
                if i + 1 >= l:
                    if 'E' not in ops[part[i]][1]:
                        return False
                elif is_upper(part[i + 1]):
                    if 'L' not in ops[part[i]][1]:
                        return False
                elif part[i + 1] not in ops[part[i]][1]:
                    return False
            elif part[i] != '<' or i + 1 != l:
                return False
            i += 1
    return True

class Inputs:
    """Class storing information about rules, queries, and initial facts given in a string.
        For each one, uses the corresponding function, and checks if the format is correct.
        Keep in track th current line read in case an error occurs to display it."""

    def __init__(self):
        self.line = 0
        self.nodes = dict()
        self.multi_rules = dict()
        self.queries = []
        self.entries = []
        self.current = "rules"

    def take_entries(self, line):
        'Takes initial facts that should be true, set them in the class. Starts with \'?\''

        if self.current != "rules":
            if self.current == "entries":
                msg = "Only one line for initial facts allowed"
            else:
                msg = "You cannot insert initial facts here, respect the order : " \
                        + "Rules => Initial facts => Queries"
            errors.parse(self.line, msg)
        if not is_upper(line):
            errors.parse(self.line, "Initial facts not well formated, only upper-case " \
                    + "alphabetical characters allowed")
        for c in line:
            self.entries.append(c)
        self.current = "entries"

    def take_queries(self, line):
        'Takes queries requiered by user, set them in the class. Starts with \'=\''

        if self.current != "entries":
            if self.current == "queries":
                msg = "Only one line for querys allowed"
            else:
                msg = "You cannot insert queries here, respect the order : " \
                        + "Rules => Initial facts => Queries"
            errors.parse(self.line, msg)
        if not is_upper(line):
            errors.parse(self.line, "Query not well formated, only upper-case alphabetical " \
                    + "characters allowed")
        for c in line:
            self.queries.append(c)
        self.current = "queries"
    
    def take_rules(self, line):
        'Takes a rule given on a line, add it to the class'

        if self.current != "rules":
            errors.parse(self.line, "You cannot insert a rule here, respect the order : " \
                    + "Rules => Initial facts => Queries")
        elif not rule_is_valid(line):
            errors.parse(self.line, "Rule is not well formated")
        eq = line.split("=>")
        if eq[0][-1] == '<':
            eq[0] = eq[0][:-1]
            equi = 1
        else:
            equi = 0
        while equi > -1:
            if len(eq[1 if equi == 0 else 0]) == 1:
                refDic = self.nodes
            else:
                refDic = self.multi_rules
            opKey = rpn.shunting(rpn.get_input(eq[1 if equi == 0 else 0]))[-1][2]
            if opKey not in refDic:
                refDic[opKey] = []
            refDic[opKey].append(rpn.shunting(rpn.get_input(eq[0 if equi == 0 else 1]))[-1][2])
            equi -= 1

    def parsing(self, content):
        'Main function called to read the content of the file'
        
        if not user_input:
            bp.print_title(" Input :")
            print(content)
        content = content.replace(" ", "")
        content = content.replace("\t", "")
        lines = content.split("\n")
        for line in lines:
            self.line += 1
            if '#' in line:
                line = line[:line.index('#')]
            if line == "":
                continue
            if line[0] == '=':
                self.take_entries(line[1:])
            elif line[0] == '?':
                self.take_queries(line[1:])
            else:
                self.take_rules(line)
