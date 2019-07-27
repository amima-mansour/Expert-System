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
    
    def process(self, rule):
        expr = []
        for r in rule:
            if isinstance(r, Node):
                if r.val or r.c in intern_queries:
                    expr.append(r.val)
                else:
                    result = self.resolve(r)
                    if result == "circle":
                        return result
                    expr.append(result)
            else:
                expr.append(r)
        result = solution.eval_postfix(expr)
        return result

    def resolve(self, goal):
        result = False
        intern_queries.append(goal.c)
        for rule in goal.rules:
            result = self.process(rule)
            if result:
                facts.append(goal.c)
                break
        if not result:
            rules = find_rules(goal.c)
            if len(rules) > 0:
                    result = self.second_resolve(rules)
        goal.val = result
        return result

    def second_resolve(self, rules):
        for key, element in rules.items():
            for rule in element:
                op = rule[0]
                result = self.process(rule[1:])
                node = created_node[key]
                if not key in intern_queries or not node.val:
                    if result and op == '+':
                        node.val = True
                        facts.append(node.c)
                        return True
                    if result == False and op == '|':
                        node.val = False
                        return False
                value = solution.reverse_eval_postfix(result, node.val, op)
                if value:
                    break
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
    dic['E'] = [['F', 'G', '|', 'H', '+']]
    dic1 = {}
    facts = ['G', 'H']
    queries = ['E']
    if len(dic):
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
