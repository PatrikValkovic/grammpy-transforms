#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 15:42
:Licence GNUv3
Part of grammpy-transforms

"""

from typing import List
from grammpy import Grammar, EPSILON, Nonterminal


def find_nonterminals_rewritable_to_epsilon(grammar: Grammar) -> List[Nonterminal]:
    rewritable = {EPSILON}
    while True:
        working = rewritable.copy()
        for rule in grammar.rules():
            allRewritable = True
            for symbol in rule.right:
                if symbol not in rewritable: allRewritable = False
            if allRewritable: working.add(rule.fromSymbol)
        if working == rewritable: break
        rewritable = working
    rewritable.remove(EPSILON)
    return [i for i in rewritable]
