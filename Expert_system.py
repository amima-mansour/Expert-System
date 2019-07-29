#!/usr/bin/Python3.4

from sys import argv as av
import errors
import parsing
import solution
import Node as node

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
s = node.Resolve(node.created_node)
i = 0
length = len(queries)
while i < length:
    n = node.created_node[queries[i]]
    if not queries[i] in facts:
        results[n.c] = s.resolve(n)
    else:
        results[n.c] = True
    i += 1
for key, element in results.items():
    print("{} => {}".format(key, element))
