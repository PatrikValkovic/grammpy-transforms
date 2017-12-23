#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.12.2017 16:05
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Nonterminal, Rule, EPSILON
from grammpy.Grammars.MultipleRulesGrammar import SplitRule


class Adding:
    def __init__(self, rule: Rule):
        self.rule = rule
        self.processed = False

    def process(self):
        child_symbols = self.rule.to_symbols
        self.processed = True
        child_rules = []
        for child in child_symbols:  # type: Nonterminal
            if child.to_rule is not None:
                child_rules.append(child.to_rule)
        return child_rules

def splitted_rules(root: Nonterminal):
    stack = list()
    stack.append(Adding(root.to_rule))
    while len(stack) > 0:
        proc = stack.pop()  # type: Adding
        if not proc.processed:
            add = proc.process()
            stack.append(proc)
            for a in add:
                stack.append(Adding(a))
        elif isinstance(proc.rule, SplitRule):
            created_rule = proc.rule.from_rule()  # type: Rule
            #Solve parents
            for s in proc.rule.from_symbols:  # type: Nonterminal
                s._set_to_rule(created_rule)
                created_rule._from_symbols.append(s)
            #Solve childs
            for ch in proc.rule.to_symbols:
                ch._set_from_rule(created_rule)
                created_rule.to_symbols.append(ch)
            stack.append(Adding(created_rule))
    return root
