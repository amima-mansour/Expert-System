#!/usr/bin/Python3.4
import solution

created_node = {}
composed_node = {}
facts = []

class Node:
    def __init__(self, c, val):
        self.c = c
        self.val = val
        self.rules = []
    
    def add_rules(self, rules, facts):
        for rule in rules:
            r = []
            rule = list(rule.replace(" ", ""))
            for element in rule:
                if element.isupper():
                    if element in created_node:
                        r.append(created_node[element])
                    else:
                        val = False
                        if element in facts:
                            val = True
                        new = Node(element, val)
                        r.append(new)
                        created_node[element] = new
                else:
                    r.append(element)
            self.rules.append(r)

intern_queries = []

class Resolve:
    def __init__(self, nodes):
        self.nodes = nodes
    
    def check_rules(self, rule, key):
        tmp = ""
        for r in rule:
            if isinstance(r, Node):
                tmp += r.c
            else:
                tmp += r
        rule = " ".join(tmp)
        key = list(key.replace(" ", ""))
        for i, r in enumerate(key):
            if r.isupper():
                key[i] = created_node[r]
        if rule in created_node:
            for r in created_node[rule].rules:
                if key  == r:
                    return rule
        if rule in composed_node:
            for r in composed_node[rule]:
                if r == key:
                    return rule
        return None

    def process(self, rule, c):
        expr = []
        for r in rule:
            if isinstance(r, Node):
                if r.c in intern_queries:
                    return False
                if r.val:
                    expr.append(r.val)
                else:
                    result = self.resolve(r)
                    expr.append(result)
            else:
                expr.append(r)
        result = solution.eval_postfix(expr)
        print("result3 = {}".format(result))
        return result

    def resolve(self, goal):
        print("goal = {}".format(goal.c))
        result = False
        intern_queries.append(goal.c)
        for rule in goal.rules:
            result = self.process(rule, goal.c)
            var = self.check_rules(rule, goal.c)
            if var and not result and var not in intern_queries:
                if len(var) == 1:
                    result = self.resolve(var)
                else:
                    result = self.second_resolve(find_rules(var), var)
            if result:
                facts.append(goal.c)
                goal.val = True
                return True
        if not result:
            rules = find_rules(goal.c)
            if len(rules) > 0:
                result = self.second_resolve(rules, goal)
        if result:
            goal.val = True
            facts.append(goal.c)
        return result

    def second_resolve(self, rules, goal):
        for key, element in rules.items():
            expr = []
            for rule in element:
                result = self.process(rule, goal.c)
                print("result2 = {}".format(result))
                var = self.check_rules(rule, key)
                if not result and var:
                    if len(var) == 1:
                        result = self.resolve(var)
                    else:
                        result = self.second_resolve(find_rules(var), var)
                k = key.replace(" ", "")
                for c in k:
                    if not c in created_node and c not in intern_queries:
                        expr.append(c)
                    elif c == goal.c:
                        expr.append(c)
                    elif c in intern_queries:
                        expr.append(created_node[c].val)
                    else:
                        expr.append(self.resolve(created_node[c]))
                value = solution.reverse_eval_postfix(result, expr, goal.c)
                if value:
                    goal.val = True
                    facts.append(goal.c)
                    print("facts = {}".format(facts))
                    return value
        return value

def storage_nodes(rules, f):
    facts = f
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

def storage_multiple_nodes(rules, f):
    facts = f
    for key, rule in rules.items():
        composed_node[key] = []
        elements = list(key.replace(" ", ""))
        for element in elements:
            if element.isupper() and element not in created_node:
                val = False
                if element in facts:
                    val = True
                new = Node(key, val)
                created_node[key] = new
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

def find_rules(node):
    rules = {}
    for key, element in composed_node.items():
        if node in key:
            rules[key] = element
    return rules


if __name__ == "__main__":
    facts = ['G', 'H']
    queries = ['E']
    if len(dic) > 0:
        storage_nodes(dic, facts, created_node)
    if len(dic1) > 0:
        storage_nodes(dic1, facts, composed_node)
    results = {}
    s = Resolve(created_node)
    i = 0
    length = len(queries)
    while i < length:
        node = created_node[queries[i]]
        if not queries[i] in facts:
            results[node.c] = s.resolve(node)
        else:
            results[node.c] = True
        i += 1
    for key, element in results.items():
        print("{} => {}".format(key, element))
