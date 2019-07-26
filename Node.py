import solution

created_node = {}
composed_node = {}

class Node:
    def __init__(self, c, val):
        self.c = c
        self.val = val
        self.rules = []
    
    def add_rules(self, rules, facts):
        for rule in rules:
            r = []
            print(rules)
            for element in rule:
                if element.isupper():
                    if element in created_node:
                        r.append(created_node[element])
                    else:
                        val = False
                        print(element)
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
    
    def process(self, rule, facts):
        expr = []
        for r in rule:
            if isinstance(r, Node):
                if r.val == True or r.c in intern_queries:
                    expr.append(r.val)
                else:
                    result = self.resolve(r, facts)
                    if result == "circle":
                        return result
                    expr.append(result)
            else:
                expr.append(r)
        result = solution.eval_postfix(expr)
        return result

    def resolve(self, goal, facts):
        intern_queries.append(goal.c)
        result = "Undetermined"
        for rule in goal.rules:
            result = self.process(rule, facts)
            print(result)
            if result == True:
                facts.append(goal.c)
                goal.val = True
                break
        if not result or result == "Undetermined":
            rules = find_rules(goal.c)
            if len(rules) > 0:
                    print(rules)
                    result = self.second_resolve(rules, facts)
        if result == "Undetermined":
            result = False
        return result

    def second_resolve(self, rules, facts):
        for key, element in rules.items():
            print(key)
            for rule in element:
                print(rule)
                print(rule[1:])
                op = rule[0]
                result = self.process(rule[1:], facts)
                node = created_node[key]
                if not key in facts or not key in intern_queries:
                    if result == True and op == '+':
                        node.val = True
                        facts.append(node.c)
                        return True
                    if result == False and op == '|':
                        node.val = False
                        return False
                    # # print("Node a chercher = {}".format(node.c))
                    # node.val = self.resolve(created_node[key], facts)
                    if node.val == True:
                        facts.append(node.c)
                value = solution.reverse_eval_postfix(result, node.val, op)
                if value == "Undetermined":
                    value = False
                if value == True:
                    break
        if value == "Undetermined":
            value = False 
        return value

def storage_nodes(rules, facts, nodes):
    for key, element in rules.items():
        if key not in created_node:
            val = False
            if key in facts:
                val = True
            new = Node(key, val)
            nodes[key] = new
            new.add_rules(element, facts)
        else:
            nodes[key].add_rules(element, facts)

def find_rules(node):
    rules = {}

    for key, element in composed_node.items():
        if node in key:
            index = key.index(node)
            rules[key[(index + 1) % 2]] = element.rules
        print(rules)
    return rules


if __name__ == "__main__":
    dic = {}
    dic['E'] = [['A', 'B', 'C', '+', '|']]
    # dic['B'] = [['D', 'E', '^']]
    # dic['A'] = [['C']]
    dic1 = {}
    # dic1['LN'] = [['+', 'O', 'P', '+']]
    facts = ['A']
    queries = ['E']
    storage_nodes(dic, facts, created_node)
    storage_nodes(dic1, facts, composed_node)
    results = {}
    # print("SIMPLE")
    # for key, element in created_node.items():
    #     print("key = {}, value = {}\nrules".format(key, element.val))
    #     for el in element.rules:
    #         for i in el:
    #             if isinstance(i, Node): 
    #                 print("{}, ".format(i.c)),
    #             else:
    #                 print("{}, ".format(i)),
    #             print("\n")
    # print("COMPOSED")
    # for key, element in composed_node.items():
    #     print("key = {}, value = {}\nrules".format(key, element.val))
    #     for el in element.rules:
    #         for i in el:
    #             if isinstance(i, Node): 
    #                 print("{}, ".format(i.c)),
    #                 print("")
    #             else:
    #                 print("{}, ".format(i)),
    #                 print("")
    #             print("\n")
    s = Resolve(created_node)
    i = 0
    length = len(queries)
    while i < length:
        node = created_node[queries[i]]
        # print(facts)
        if not queries[i] in facts:
            value = s.resolve(node, facts)
            print("value 1 = {}".format(value))
            rules = find_rules(node.c)
            if not value and len(rules) > 0:
                value_2 = s.second_resolve(rules, facts)
                print("value 1 = {}".format(value_2))
                if value_2 == True:
                    value = value_2
        else:
            value = True
        #if value:
        #    facts.append(node.c)
        # print("{} => {}".format(node.c, value))
        results[node.c] = value
        node.val = value
        # print(facts) 
        i += 1
    for key, element in results.items():
        print("{} => {}".format(key, element))
