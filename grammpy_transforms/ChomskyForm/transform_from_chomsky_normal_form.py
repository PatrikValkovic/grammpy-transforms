#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 03.09.2017 10:46
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import *
from .transform_to_chomsky_normal_form import *


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


def transform_from_chomsky_normal_form(root: Nonterminal):
    stack = list()
    stack.append(Adding(root.to_rule))
    while len(stack) > 0:
        proc = stack.pop()  # type: Adding
        if not proc.processed:
            add = proc.process()
            stack.append(proc)
            for a in add:
                stack.append(Adding(a))
        elif isinstance(proc.rule, ChomskyTermRule):
            upper_nonterm = proc.rule.from_symbols[0]  # type: Nonterminal
            to_append = upper_nonterm.from_rule  # type: Rule
            index = to_append.to_symbols.index(upper_nonterm)
            term = proc.rule.to_symbols[0]  # type: Terminal
            to_append.to_symbols[index] = term
            term._set_from_rule(to_append)
        elif isinstance(proc.rule, ChomskyTerminalReplaceRule):
            to_rule = proc.rule.from_rule()  # type: Rule
            for p in proc.rule.from_symbols:  # type: Nonterminal
                to_rule._from_symbols.append(p)
                p._set_to_rule(to_rule)
            for c in proc.rule.to_symbols:  # type: Nonterminal
                to_rule._to_symbols.append(c)
                c._set_from_rule(to_rule)
            add = Adding(to_rule)
            add.processed = True
            stack.append(add)
        elif isinstance(proc.rule, ChomskySplitRule):
            created_rule = proc.rule.from_rule()  # type: Rule
            #parent nonterminals
            for p in proc.rule.from_symbols:  # type: Nonterminal
                p._set_to_rule(created_rule)
                created_rule._from_symbols.append(p)
            #left child
            left_child = proc.rule.to_symbols[0] # type: Nonterminal
            left_child._set_from_rule(created_rule)
            created_rule._to_symbols.append(left_child)
            #right childs
            for ch in proc.rule.to_symbols[1].to_rule.to_symbols:  # type: Nonterminal
                ch._set_from_rule(created_rule)
                created_rule.to_symbols.append(ch)
            add = Adding(created_rule)
            add.processed = True
            stack.append(add)
    return root