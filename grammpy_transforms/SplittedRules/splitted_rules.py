#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.12.2017 16:05
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Nonterminal, Rule, EPSILON
from grammpy.Grammars.MultipleRulesGrammar import SplitRule
from ..Manipulations import Manipulations, Traversing

def splitted_rules(root: Nonterminal):
    items = Traversing.postOrder(root)
    items = filter(lambda x: isinstance(x, Rule), items)
    for i in items:
        if not isinstance(i, SplitRule):
            continue
        newRule = i.from_rule()
        Manipulations.replace(i, newRule)
    return root
