#!/usr/bin/Python3.4

# dict of all created nodes for example created_node['A'] = node
created_node = {}
# dict of all composed conclusions such as A + B => C + D, for example composed_node['C  D +'] = [[A, B, '+']]. A and B are nodes
composed_node = {}


class Node:
    """
        Node Class has :
        argument c : an uppercase
        argument val : boolean value (true/false)
        argment rules : list of all rules taht apply to Node
    """
    def __init__(self, c, val):
        self.c = c
        self.val = val
        self.rules = []
    
    def add_rules(self, rules, facts):
        """
            add rules to the node from the initial dict of rules
            which c of class node is the key of rules
        """
        for rule in rules:
            r = []
            rule = list(rule.replace(" ", ""))
            for element in rule:
                if element.isupper():
                    if element in created_node:
                        # if element is already created as node, we change it to the node 
                        r.append(created_node[element])
                    else:
                        # else we created a new node 
                        val = False
                        if element in facts:
                            val = True
                        new = Node(element, val)
                        r.append(new)
                        # we add the new node to created_node
                        created_node[element] = new
                else:
                    r.append(element)
            self.rules.append(r)

def storage_nodes(rules, facts):
    for key, element in rules.items():
        if key not in created_node:
            val = False
            if key in facts:
                val = True
            new = Node(key, val)
            created_node[key] = new
            new.add_rules(element, facts)
        else:
            created_node[key].add_rules(element, facts)

def storage_multiple_nodes(rules, facts):
    for key, rule in rules.items():
        composed_node[key] = []
        elements = list(key.replace(" ", ""))
        for element in elements:
            if element.isupper() and element not in created_node:
                val = False
                if element in facts:
                    val = True
                new = Node(element, val)
                created_node[element] = new
        for element_list in rule:
            element_list = list(element_list.replace(" ", ""))
            rule_list = []
            for element in element_list:
                if not element.isupper():
                    rule_list.append(element)
                elif element not in created_node:
                    val = False
                    if element in facts:
                        val = True
                    new = Node(element, val)
                    created_node[element] = new
                    rule_list.append(new)
                else:
                    rule_list.append(created_node[element])
            composed_node[key].append(rule_list)
