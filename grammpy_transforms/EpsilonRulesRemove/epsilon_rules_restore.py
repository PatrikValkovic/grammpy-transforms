#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 03.09.2017 10:47
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import *
from .remove_rules_with_epsilon import EpsilonRemovedRule

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

def _restore_tree_for(root: Nonterminal, translate: dict):
    if root is EPSILON:
        return EPSILON
    created_nonterm = root()  # type: Nonterminal
    created_rule = translate[root]()  # type: Rule
    created_nonterm._set_to_rule(created_rule)
    created_rule._from_symbols.append(created_nonterm)
    for ch in created_rule.right:
        p = _restore_tree_for(ch, translate)  # type: Nonterminal
        if p is not EPSILON:
            p._set_from_rule(created_rule)
        created_rule._to_symbols.append(p)
    return created_nonterm

def epsilon_rules_restore(root: Nonterminal):
    stack = list()
    stack.append(Adding(root.to_rule))
    while len(stack) > 0:
        proc = stack.pop()  # type: Adding
        if not proc.processed:
            add = proc.process()
            stack.append(proc)
            for a in add:
                stack.append(Adding(a))
        elif isinstance(proc.rule, EpsilonRemovedRule):
            created_rule = proc.rule.from_rule()  # type: Rule
            #Solve parents
            for s in proc.rule.from_symbols:  # type: Nonterminal
                s._set_to_rule(created_rule)
                created_rule._from_symbols.append(s)
            #Copy childs to replace index
            for i in range(proc.rule.replace_index):
                ch = proc.rule.to_symbols[i]  # type: Nonterminal
                ch._set_from_rule(created_rule)
                created_rule._to_symbols.append(ch)
            #Add epsilon
            symb = _restore_tree_for(created_rule.right[proc.rule.replace_index], proc.rule.backtrack) # type: Nonterminal
            created_rule._to_symbols.append(symb)
            if symb is not EPSILON:
                symb._set_from_rule(created_rule)
            #Add rest of childs
            for i in range(proc.rule.replace_index, len(proc.rule.to_symbols)):
                ch = proc.rule.to_symbols[i]  # type: Nonterminal
                ch._set_from_rule(created_rule)
                created_rule._to_symbols.append(ch)
    return root