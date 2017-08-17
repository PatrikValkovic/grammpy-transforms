#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.06.2017 16:39
:Licence GNUv3
Part of grammpy-transforms

"""

from copy import copy
from grammpy import Grammar


def _copy_grammar(grammar):
    return copy(grammar)

def remove_nongenerating_symbol(grammar: Grammar, transform_grammar=False) -> Grammar:
    if transform_grammar is False:
        grammar = _copy_grammar(grammar)
    generates = set(item.s for item in grammar.terms())
    while True:
        additional = generates.copy()
        for rule in grammar.rules():
            rightPart = rule.right
            allIn = True
            for symbol in rightPart:
                if symbol not in generates:
                    allIn = False
            if not allIn:
                continue
            additional.add(rule.fromSymbol)
        if additional == generates:
            break
        generates = additional
    allNonterms = list(grammar.nonterms())
    for nonterm in allNonterms:
        if nonterm not in generates:
            grammar.remove_nonterm(nonterm)
    return grammar
