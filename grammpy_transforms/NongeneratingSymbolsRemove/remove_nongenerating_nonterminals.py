#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 10.08.2017 20:33
:Licence GNUv3
Part of grammpy-transforms

"""

from copy import copy
from grammpy import Grammar, EPSILON

def remove_nongenerating_nonterminals(grammar: Grammar, transform_grammar=False) -> Grammar:
    """
    Remove nongenerating symbols from the grammar
    :param grammar: Grammar where to remove nongenerating symbols
    :param transform_grammar: True if transformation should be performed in place, false otherwise.
    False by default.
    :return: Grammar without nongenerating symbols
    """
    # Copy if required
    if transform_grammar is False: grammar = copy(grammar)
    # Create working sets
    generates = set(item.s for item in grammar.terms())
    generates.add(EPSILON)
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
