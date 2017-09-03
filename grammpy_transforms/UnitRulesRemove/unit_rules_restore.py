#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 03.09.2017 10:48
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import *
from .remove_unit_rules import ReducedUnitRule


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


def unit_rules_restore(root: Nonterminal):
    stack = list()
    stack.append(Adding(root.to_rule))
    while len(stack) > 0:
        proc = stack.pop()  # type: Adding
        if not proc.processed:
            add = proc.process()
            stack.append(proc)
            for a in add:
                stack.append(Adding(a))
        elif isinstance(proc.rule, ReducedUnitRule):
            parent_nonterm = proc.rule.from_symbols[0]  # type: Nonterminal
            created_rule = None
            # restore chain
            for r in proc.rule.by_rules:
                created_rule = r()  # type: Rule
                parent_nonterm._set_to_rule(created_rule)
                created_rule._from_symbols.append(parent_nonterm)
                created_nonterm = r.toSymbol() # type: Nonterminal
                created_rule._to_symbols.append(created_nonterm)
                created_nonterm._set_from_rule(created_rule)
                parent_nonterm = created_nonterm
            # restore last rule
            last_rule = proc.rule.end_rule()  # type: Rule
            last_rule._from_symbols.append(parent_nonterm)
            parent_nonterm._set_to_rule(last_rule)
            for ch in proc.rule.to_symbols: # type: Nonterminal
                ch._set_from_rule(last_rule)
                last_rule._to_symbols.append(ch)
            add = Adding(last_rule)
            add.processed = True
            stack.append(add)
    return root

