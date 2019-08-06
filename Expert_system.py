#!/usr/bin/Python3.4

from sys import argv as av
import errors
import parsing
import RPN_calc
import node
import resolve as res
import beautiful_print as bp
import colors

in_progress = True

if len(av) > 1 and av[1].startswith('-'):
    if not parsing.valid_arg(av[1]):
        errors.usage()
    else:
        if 'd' in av[1]:
            res.display = True
        if 'i' in av[1]:
            if len(av) != 2:
                errors.usage()
            parsing.user_input = True
        elif len(av) != 3:
            errors.usage()
        else:
            argu = av[2]
elif len(av) == 2:
    argu = av[1]
else:
    errors.usage()
if not parsing.user_input:
    content = parsing.file_opener(argu)
else:
    content = parsing.get_input()
while in_progress == True:
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
            if queries[i] in facts:
                results[queries[i]] = True
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
    if parsing.user_input:
        try:
            continue_progress = input(colors.green + "Do you want to try another input ? (Y to continue)\n" \
                    + colors.normal)
        except:
            errors.stoped_input()
        if continue_progress != 'Y':
            in_progress = False
            print(colors.green + "See you later !" + colors.normal)
        else:
            content = parsing.get_input()
            node.created_node = {}
            node.composed_node = {}
            res.intern_queries = []
    else:
        break
