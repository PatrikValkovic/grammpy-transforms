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
    """
    Transform rules created by Chomsky Normal Form to original rules used in grammar.
    :param root: Root of AST
    :return: Modified AST
    """
    items = Traversing.postOrder(root)
    items = filter(lambda x: isinstance(x, (ChomskyTermRule,ChomskyTerminalReplaceRule)), items)
    de = deque(items)
    while de:
        rule = de.popleft()
        if isinstance(rule, ChomskyTermRule):
            upper_nonterm = rule.from_symbols[0]  # type: Nonterminal
            term = rule.to_symbols[0]
            Manipulations.replaceNode(upper_nonterm, term)
        elif isinstance(rule, ChomskyTerminalReplaceRule):
            created_rule = rule.from_rule()  # type: Rule
            Manipulations.replaceRule(rule, created_rule)
            de.append(created_rule)

    items = Traversing.postOrder(root)
    items = filter(lambda x: isinstance(x, ChomskySplitRule), items)
    de = deque(items)
    while de:
        rule = de.popleft()
        if isinstance(rule, ChomskySplitRule):
            created_rule = rule.from_rule()  # type: Rule
            # parent nonterminals
            for p in rule.from_symbols:  # type: Nonterminal
                p._set_to_rule(created_rule)
                created_rule._from_symbols.append(p)
            # left child
            left_child = rule.to_symbols[0]  # type: Nonterminal
            left_child._set_from_rule(created_rule)
            created_rule._to_symbols.append(left_child)
            # right childs
            for ch in rule.to_symbols[1].to_rule.to_symbols:  # type: Nonterminal
                ch._set_from_rule(created_rule)
                created_rule.to_symbols.append(ch)
            de.append(created_rule)
    return root