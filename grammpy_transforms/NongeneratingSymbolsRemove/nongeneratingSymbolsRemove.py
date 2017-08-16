#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.06.2017 16:39
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Grammar


def _copy_grammar(grammar):
    return Grammar(terminals=grammar.terms(),
                   nonterminals=grammar.nonterms(),
                   rules=grammar.rules(),
                   start_symbol=grammar.start_get())


def remove_nongenerating_symbol(grammar: Grammar, transform_grammar=False) -> Grammar:
    if transform_grammar is True:
        grammar = _copy_grammar(grammar)
    generates = set(grammar.terms())
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
            for symbol in rule.left:
                additional.add(symbol)
        if additional == generates:
            break
        generates = additional
    allNonterms = list(grammar.nonterms())
    for nonterm in allNonterms:
        if nonterm not in generates:
            grammar.remove_nonterm(nonterm)
    return grammar
