#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 15:42
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Grammar, EPSILON


def find_nonterminals_rewritable_to_epsilon(grammar: Grammar) -> dict:
    rewritable = dict()
    rewritable[EPSILON] = None
    while True:
        working = rewritable.copy()
        for rule in grammar.rules():
            allRewritable = True
            for symbol in rule.right:
                if symbol not in rewritable: allRewritable = False
            if allRewritable and rule.fromSymbol not in working:
                working[rule.fromSymbol] = rule
        if working == rewritable: break
        rewritable = working
    del rewritable[EPSILON]
    return rewritable
