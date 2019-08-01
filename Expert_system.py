#!/usr/bin/Python3.4

from sys import argv as av
import errors
import parsing
import RPN_calc
import node
import resolve as res
import beautiful_print as bp

if len(av) != 2:
    errors.usage()
content = parsing.file_opener(av[1])
if content is "":
    errors.empty(av[1])
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
