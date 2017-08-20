#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 10.08.2017 20:33
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Grammar
from .NongeneratingSymbolsRemove import remove_nongenerating_symbols
from .UnreachableSymbolsRemove import remove_unreachable_symbols
from .EpsilonRulesRemove import remove_rules_with_epsilon, find_terminals_rewritable_to_epsilon


class ContextFree:
    @staticmethod
    def remove_nongenerating_symbols(grammar: Grammar, transform_grammar=False):
        return remove_nongenerating_symbols(grammar, transform_grammar)

    @staticmethod
    def is_grammar_generating(grammar: Grammar, transform_grammar=False, perform_remove=True):
        g = grammar
        if perform_remove:
            g = ContextFree.remove_nongenerating_symbols(grammar, transform_grammar=transform_grammar)
        return g.start_get() in g.nonterms()

    @staticmethod
    def remove_unreachable_symbols(grammar: Grammar, transform_grammar=False):
        return remove_unreachable_symbols(grammar, transform_grammar)

    @staticmethod
    def remove_useless_symbols(grammar: Grammar, transform_grammar=False, *,
                                   perform_unreachable_alg = True,
                                   perform_nongenerating_alg = True) -> Grammar:
        if perform_nongenerating_alg:
            grammar = ContextFree.remove_nongenerating_symbols(grammar, transform_grammar=transform_grammar)
            transform_grammar = True
        if perform_unreachable_alg:
            grammar = ContextFree.remove_unreachable_symbols(grammar, transform_grammar=transform_grammar)
        return grammar

    @staticmethod
    def remove_rules_with_epsilon(grammar: Grammar, transform_grammar=True) -> Grammar:
        return remove_rules_with_epsilon(grammar, transform_grammar=transform_grammar)

    @staticmethod
    def find_terminals_rewritable_to_epsilon(grammar: Grammar) -> list:
        return find_terminals_rewritable_to_epsilon(grammar)