import re
import argparse

def parsing_test(string):
    while string and '(' in string:
        key = string.index('(')
        part = string[:key]
        string = string[key + 1:]
        if part and not re.match(r"^(!)?[A-Z]([\+\^\|])?$", part):
            return False
        if ')' in string:
            key = len(string) - string[::-1].index(')') - 1
            part = string[key + 1:]
            string = string[:key]
            if part and not re.match(r"^([\+\^\|](!)?[A-Z])*$", part):
                return False
    if string and not re.match(r"^(!)?[A-Z]([\+\^\|](!)?[A-Z])*$", string):
        return False
    return True

parser = argparse.ArgumentParser(description='EXPERT SYSTEM @ 42')
parser.add_argument("input", help="input file", type=argparse.FileType('r'))
args = parser.parse_args()
data = args.input.read().splitlines()
args.input.close()
data = [x for x in data if x[0] != '#']
# parsing
rules = []
for el in data:
    el = filter(None, re.split(r'#.*', el))[0]
    if ">" in el:
        left, right = re.split("=>|<=>", el)
        left = left.replace(" ", "")
        if not parsing_test(left):
            print "ERROR SYNTAX {}".format(left)
            exit()
        # left = re.split("([^A-Z])", left.replace(" ", ""))
        # left = [x for x in left if x]
        # right = re.split("([^A-Z])", right.replace(" ", ""))=
        # right = [x for x in right if x]
        # print left, right
    elif el[0] == '=':
        facts = list(el[1:].replace(" ", ""))
    elif el[0] == '?':
        queries = list(el[1:].replace(" ", ""))
    else:
        print "ERROR"
        exit()
if len(rules) == 0 or len(facts) == 0 or len(queries) == 0:
    print "ERROR"
    exit()

# Syntax Error => OK
# Wrong character => OK
# NO => or <=> in a rule
# No respect of the rule : Alphabatic character + operator only for negation : match expression = r"(!)?[A-Z]([\+\^\|](!)?[A-Z])*" => OK
# Contradiction : How to resolve them