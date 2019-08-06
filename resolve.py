#!/usr/bin/Python3.4
import RPN_calc
import errors
import node
import colors

# list of nodes whose value has already been found or being searched
intern_queries = []
# MAKE IT BEAUTIFUL
tab = "\t" + colors.bg_blue + " " + colors.normal
space_mountain = colors.bg_blue + " " + colors.normal
display = False

class Resolve:
    def __init__(self, nodes):
        self.nodes = nodes
#        intern_queries = []
    
    def check_rules(self, rule, key):
        """
            check if we have an equivalence rule
            we have a key and a rule and we check if we have rule in node.composed_node
            with key is the rule and the rule is the key
        """
        # transform a rule in the form of the key
        # rule : [A, B, +] => key : 'A B +'
        tmp = ""
        for r in rule:
            if isinstance(r, node.Node):
                tmp += r.c
            else:
                tmp += r
        rule = " ".join(tmp)
        # transform a key in the form of the rule
        # key : 'A B +' => rule : [A, B, +] 
        key = list(key.replace(" ", ""))
        for i, r in enumerate(key):
            if r.isupper():
                key[i] = node.created_node[r]
        # we check if rule is a key in node.created_node
        # if it is, we return the node : node.created_node[rule] 
        if rule in node.created_node:
            for r in node.created_node[rule].rules:
                if key  == r:
                    return node.created_node[rule]
        # we check if rule is a key in node.composed_node
        # if it is, we return the rule under a string form 
        if rule in node.composed_node:
            for r in node.composed_node[rule]:
                if r == key:
                    return rule
        return None

    def process(self, rule, c):
        """
            Takes the expr <list> and <char>
            transform a rule : [A, B, '+'] in list with only boolean values and operators
            like [True, False, '+'] and return the result of the evaluation of the list
        """
        expr = []
        for r in rule:
            if isinstance(r, node.Node):
                if r.val == True:
                    expr.append(r.val)
                elif r.c in intern_queries and r.c != c:
                    expr.append(r.val)
                else:
                    # in this case, the value of r is not known yet
                    # we have to call the resolve function
                    self.resolve(r)
                    # at the end of the search, we append its value in our list expression
                    expr.append(r.val)
            else:
                expr.append(r)
        return(RPN_calc.eval_postfix(expr))

    def resolve(self, goal):
        """
            Takes the expr <Node>
            search the value(True/false/Undetermined) of goal
        """
        # In order to avoid an infinite loop of search  
        if goal.c in intern_queries or goal.val == True:
            return
        if display:
            global space_mountain
            print(space_mountain + "We're looking for " + colors.cyan + goal.c + colors.normal)
            space_mountain += tab
        # Every time we search for the value of a node, we put its goal.c in intern_queries
        intern_queries.append(goal.c)
        goal.val = None
        # this dict is set to have a value for f => equivalent result and a value for t => implication result
        tmp = {'f': None, 't':False}
        # we check all the rules in goal.rules except in the case of conflict
        for rule in goal.rules:
            if display:
                print(space_mountain + colors.purple + rule_to_key(rule) + " => " + goal.c + colors.normal)
            # we search of the evaluation of the rule and we put it in a temprory value
            tmp['t'] = self.process(rule, goal.c)
            if tmp['t'] == True and tmp['t'] != tmp['f'] and tmp['f'] is not None:
                errors.conflict(goal.c)
            # we check here if we have an equivalence
            var = self.check_rules(rule, goal.c)
            if var:
                if  isinstance(var, node.Node):
                    # if we are in the first case and we have a node, so we will search for its value and put it temp
                    self.resolve(var)
                    tmp['f'] = var.val
                else:
                    # if we are in the second case and we have a strind, so we will search for the rule that correspond
                    rules = find_rules(var)
                    key = find_key(rule)
                    # this to avoid an infinite loop if we have this  case A + B => A + B
                    if key in rules and rule in rules[key]:
                        if display:
                            space_mountain = space_mountain[:-11]
                            print(space_mountain + "Value set to " + colors.cyan + "{}".format(goal.val) + colors.normal)
                        return
                    tmp['f'] = self.complexe_resolve(rules, goal, rule_to_key(rule))
                if tmp['t'] == True and tmp['t'] != tmp['f'] and tmp['f'] is not None:
                    errors.conflict(goal.c)
            elif tmp['t'] == True:
                tmp['f'] = True
        # in this step, we search rules in our node.composed_nodes and check or search value 
        rules = find_rules(goal.c)
        if len(rules) > 0:
            self.complexe_resolve(rules, goal, None)
        if (tmp['f'] is not None and goal.val is not None and tmp['f'] != goal.val) or (tmp['f'] is None and tmp['t'] and goal.val == False):
            errors.conflict(goal.c)
        if goal.val is None and tmp['f'] is not None:
            goal.val = tmp['f']
        elif goal.val is None and tmp['t'] is not None:
            goal.val = tmp['t']
        elif goal.val == None:
            goal.val = False
        if display:
            space_mountain = space_mountain[:-11]
            print(space_mountain + "Value set to " + colors.cyan + "{}".format(goal.val) + colors.normal)
        
             
    def complexe_resolve(self, rules, goal, key_tmp):
        """
            Takes the expr <dict>, <Node> and <str>
            search the value(True/false/Undetermined) of goal in composed rules
        """
        for key, element in rules.items():
            expr = []
            if key_tmp == key:
                continue
            if display:
                global space_mountain
                print(space_mountain + "We're looking for " + colors.cyan + key + colors.normal)
                space_mountain += tab
            for rule in element:
                if display:
                    print(space_mountain + colors.purple + rule_to_key(rule) + " => " + key + colors.normal)
                # we evaluate the first part of the predicat
                temp = self.process(rule, goal.c)
                # we check if there is an equivalence for the rule
                var = self.check_rules(rule, key)
                temp1 = None
                if var:
                    if isinstance(var, node.Node):
                        self.resolve(var)
                        temp1 = var.val
                    else:
                        rules = find_rules(var)
                        k1 = find_key(rule)
                        if k1 in rules and rule in rules[k1]:
                            if display:
                                space_mountain = space_mountain[:-11]
                                print(space_mountain + "Value set to " + colors.cyan + "{}".format(temp) + colors.normal)
                            return
                        temp1 = self.complexe_resolve(find_rules(var), goal, rule_to_key(rule))
                elif temp == False:
                    continue
                if temp1 is not None:
                    temp = temp1
                # k is the key without space
                k = key.replace(" ", "")
                for c in k:
                    if c.isupper():
                        next_index = k.index(c) + 1
                        n = node.created_node[c]
                        if temp and k[-1] == '+':
                            # in this case we check if we have an and in the conclusion part(key) and we have a temp true
                            # A + B = True <=> A = True And B = True
                            val = True
                            if  next_index < len(k) and k[next_index] == '!':
                                val = False
                            if (n.val == True and val == False) or (n.c != goal.c and n.val == False and n.c in intern_queries and val == True): 
                                errors.conflict(n.c)
                            else:
                                n.val = val
                            expr.append(n.val)
                            if n.c not in intern_queries:
                                intern_queries.append(n.c)
                        elif temp == False and k[-1] == '|':
                            # in this case we check if we have an oor in the conclusion part(key) and we have a temp false
                            # A | B = False <=> A = False And B = False
                            val = False 
                            if  next_index < len(k) and k[next_index] == '!':
                                val = True
                            if (n.val == True and val == False) or (n.c != goal.c and n.val == False and n.c in intern_queries and val == True):
                                errors.conflict(n.c)
                            else:
                                n.val = val
                            expr.append(n.val)
                            if n.c not in intern_queries:
                                intern_queries.append(n.c)
                        elif n.val and n.c != goal.c:
                            expr.append(n.val)
                        elif c == goal.c:
                            # print("c = {} 2".format(c))
                            expr.append(c)
                        elif n.c in intern_queries:
                            # print("c = {} 3".format(c))
                            expr.append(n.val)
                        else:
                            # print("c = {} 4".format(c))
                            self.resolve(n)
                            expr.append(n.val)
                    else:
                        expr.append(c)
                if  goal.c in expr and None not in expr:
                    # if we have temp True and goal has not a definite value, we seek for goal value 
                    value = RPN_calc.reverse_eval_postfix(temp, expr, goal.c)
                    goal.val = value
            if display:
                space_mountain = space_mountain[:-11]
                print(space_mountain + "Value set to " + colors.cyan + "{}".format(temp) + colors.normal)

def find_rules(n):
    """
        Takes the expr <char>
        returns all the rules which the n is in the key
    """
    rules = {}
    for key, element in node.composed_node.items():
        if n in key:
            rules[key] = element
    return rules

def find_key(rule):
    """
        Takes the expr <dict>
        returns the key of the rule in composed_node if it is exists 
    """
    for key, element in node.composed_node.items():
        if rule in element:
            return key
    return None

def rule_to_key(rule):
    """
        Takes the expr <list>
        returns the key of a rule in a string 
    """
    key = ""
    for element in rule:
        if  isinstance(element, node.Node):
            key += element.c
        else:
            key += element
    return " ".join(key)
