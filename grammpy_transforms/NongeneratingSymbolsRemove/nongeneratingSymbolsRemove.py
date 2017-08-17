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


def remove_nongenerating_symbols(grammar: Grammar, transform_grammar=False) -> Grammar:
    # Copy if required
    if transform_grammar is False: grammar = _copy_grammar(grammar)
    # Create working sets
    generates = set(item.s for item in grammar.terms())
    rules = set(rule for rule in grammar.rules())
    while True:
        # Create set of next iteration
        additional = generates.copy()
        processedRules = []
        # Iterate over unprocessed rules
        for rule in rules:
            rightPart = rule.right
            allIn = True
            # Check if all symbols on the right part of rule are in generates set
            for symbol in rightPart:
                if symbol not in generates:
                    allIn = False
                    break
            # Symbol is missing so rule is not process
            if not allIn: continue
            # Rule is process - remove it from processing rules and make symbol as generating
            additional.add(rule.fromSymbol)
            processedRules.append(rule)
        # End of rules iterations
        # Remove process rules in current iteration
        for item in processedRules: rules.remove(item)
        # If current and previous iterations are same, than end iterations
        if additional == generates: break
        # Swap sets from previous and current iterations
        generates = additional
    # Remove nonterms that are not generating
    for nonterm in set(grammar.nonterms()).difference(generates):
        grammar.remove_nonterm(nonterm)
    return grammar
