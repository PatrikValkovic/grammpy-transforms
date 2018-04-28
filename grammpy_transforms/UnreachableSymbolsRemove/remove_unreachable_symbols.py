#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 17.08.207 13:29
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Grammar
from grammpy.exceptions import NotNonterminalException
from copy import copy


class StartSymbolNotSpecifiedException(Exception):
    pass


def remove_unreachable_symbols(grammar: Grammar, transform_grammar=False) -> Grammar:
    """
    Remove unreachable symbols from the gramar
    :param grammar: Grammar where to symbols remove
    :param transform_grammar: True if transformation should be performed in place, false otherwise.
    False by default.
    :return: Grammar without unreachable symbols.
    """
    # Copy if required
    if transform_grammar is False: grammar = copy(grammar)
    # Check if start symbol is set
    if not grammar.start_isSet(): raise StartSymbolNotSpecifiedException()
    # Create process sets
    reachable = {grammar.start_get()}
    rules = grammar.rules()
    # Begin iterations
    while True:
        # Create sets for current iteration
        active = reachable.copy()
        processedRules = []
        # Loop rest of rules
        for rule in rules:
            # If left part of rule already in reachable symbols
            if rule.fromSymbol in reachable:
                # Set symbols as reachable
                processedRules.append(rule)
                for symbol in rule.right: active.add(symbol)
        # End of rules loop
        # Remove processed rules
        for item in processedRules: rules.remove(item)
        # If current and previous iterations are same, than end iterations
        if active == reachable: break
        reachable = active
    # End of iterations
    # Set symbols to remove
    allSymbols = set(grammar.nonterms()).union(set(x.s for x in grammar.terms()))
    for symbol in allSymbols.difference(reachable):
        try:
            grammar.remove_nonterm(symbol)
        except NotNonterminalException:
            grammar.remove_term(symbol)
    return grammar
