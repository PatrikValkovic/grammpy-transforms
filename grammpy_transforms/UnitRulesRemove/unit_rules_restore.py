#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 03.09.2017 10:48
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import *
from .remove_unit_rules import ReducedUnitRule
from ..Manipulations import Manipulations, Traversing


def unit_rules_restore(root: Nonterminal):
    items = Traversing.postOrder(root)
    items = filter(lambda x: isinstance(x, ReducedUnitRule), items)
    for rule in items:
        parent_nonterm = rule.from_symbols[0]  # type: Nonterminal
        created_rule = None
        # restore chain
        for r in rule.by_rules:
            created_rule = r()  # type: Rule
            parent_nonterm._set_to_rule(created_rule)
            created_rule._from_symbols.append(parent_nonterm)
            created_nonterm = r.toSymbol() # type: Nonterminal
            created_rule._to_symbols.append(created_nonterm)
            created_nonterm._set_from_rule(created_rule)
            parent_nonterm = created_nonterm
        # restore last rule
        last_rule = rule.end_rule()  # type: Rule
        last_rule._from_symbols.append(parent_nonterm)
        parent_nonterm._set_to_rule(last_rule)
        for ch in rule.to_symbols:  # type: Nonterminal
            ch._set_from_rule(last_rule)
            last_rule._to_symbols.append(ch)
    return root

