#!/usr/bin/Python3.4

from sys import argv as av
import errors
import parsing
import RPN_calc
import node
import resolve as res
import beautiful_print as bp

if len(av) == 3 and av[1] == "-d":
    argu = av[2]
    res.display = True
elif len(av) != 2:
    errors.usage()
else:
    if parsing.valid_arg(av[1]):
        parsing.user_input = True
        if 'd' in av[1]:
            res.display = True
    else:
        argu = av[1]
if not parsing.user_input:
    content = parsing.file_opener(argu)
else:
    content = parsing.get_input()
if content is "":
    errors.empty(argu)
inputs = parsing.Inputs()
inputs.parsing(content)
facts = inputs.entries
queries = inputs.queries
dic1 = inputs.nodes
dic2 = inputs.multi_rules
if len(dic1) > 0:
    node.storage_nodes(dic1, facts)
if len(dic2) > 0:
    node.storage_multiple_nodes(dic2, facts)
results = {}
s = res.Resolve(node.created_node)
if res.display:
    bp.print_title("Resolution :")
i = 0
length = len(queries)
while i < length:
    if queries[i] not in node.created_node:
        results[queries[i]] = False
    else:
        n = node.created_node[queries[i]]
        if queries[i] in facts or n.c in res.intern_queries:
            results[n.c] = n.val
        else:
            s.resolve(n)   
            results[n.c] = n.val
    i += 1
bp.print_title("Results : ")
for key, element in results.items():
    print("{} => {}".format(key, element))
