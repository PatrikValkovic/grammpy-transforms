#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 03.09.2017 10:46
:Licence GNUv3
Part of grammpy-transforms

"""
from collections import deque

from grammpy import *
from .transform_to_chomsky_normal_form import *
from ..Manipulations import Traversing, Manipulations

def transform_from_chomsky_normal_form(root: Nonterminal):
    items = Traversing.postOrder(root)
    items = filter(lambda x: isinstance(x, (ChomskyTermRule,ChomskyTerminalReplaceRule, ChomskySplitRule)), items)
    de = deque(items)
    while de:
        rule = de.popleft()
        if isinstance(rule, ChomskyTermRule):
            upper_nonterm = rule.from_symbols[0]  # type: Nonterminal
            to_append = upper_nonterm.from_rule  # type: Rule
            index = to_append.to_symbols.index(upper_nonterm)
            term = rule.to_symbols[0]  # type: Terminal
            to_append.to_symbols[index] = term
            term._set_from_rule(to_append)
        elif isinstance(rule, ChomskyTerminalReplaceRule):
            to_rule = rule.from_rule()  # type: Rule
            for p in rule.from_symbols:  # type: Nonterminal
                to_rule._from_symbols.append(p)
                p._set_to_rule(to_rule)
            for c in rule.to_symbols:  # type: Nonterminal
                to_rule._to_symbols.append(c)
                c._set_from_rule(to_rule)
            de.append(to_rule)
        elif isinstance(rule, ChomskySplitRule):
            created_rule = rule.from_rule()  # type: Rule
            #parent nonterminals
            for p in rule.from_symbols:  # type: Nonterminal
                p._set_to_rule(created_rule)
                created_rule._from_symbols.append(p)
            #left child
            left_child = rule.to_symbols[0] # type: Nonterminal
            left_child._set_from_rule(created_rule)
            created_rule._to_symbols.append(left_child)
            #right childs
            for ch in rule.to_symbols[1].to_rule.to_symbols:  # type: Nonterminal
                ch._set_from_rule(created_rule)
                created_rule.to_symbols.append(ch)
            de.append(created_rule)
    return root