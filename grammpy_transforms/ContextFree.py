#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 10.08.2017 20:33
:Licence GNUv3
Part of grammpy-transforms

"""

from typing import List
from grammpy import *
from .NongeneratingSymbolsRemove import *
from .UnreachableSymbolsRemove import *
from .EpsilonRulesRemove import *
from .UnitRulesRemove import *
from .ChomskyForm import *

__all__ = ['ContextFree']


class ContextFree:

    EpsilonRemovedRule = EpsilonRemovedRule
    ReducedUnitRule = ReducedUnitRule
    ChomskyRule = ChomskyRule
    ChomskySplitRule = ChomskySplitRule
    ChomskyTermRule = ChomskyTermRule
    ChomskyRestRule = ChomskyRestRule
    ChomskyTerminalReplaceRule = ChomskyTerminalReplaceRule

    ChomskyNonterminal = ChomskyNonterminal
    ChomskyGroupNonterminal = ChomskyGroupNonterminal
    ChomskyTermNonterminal = ChomskyTermNonterminal

    UnitSymbolRechablingResults = UnitSymbolRechablingResults

    @staticmethod
    def remove_nongenerating_nonterminals(grammar: Grammar, transform_grammar=False):
        return remove_nongenerating_nonterminals(grammar, transform_grammar)

    @staticmethod
    def is_grammar_generating(grammar: Grammar, transform_grammar=False, perform_remove=True):
        g = grammar
        if perform_remove:
            g = ContextFree.remove_nongenerating_nonterminals(grammar, transform_grammar=transform_grammar)
        return g.start_get() in g.nonterms()

    @staticmethod
    def remove_unreachable_symbols(grammar: Grammar, transform_grammar=False):
        return remove_unreachable_symbols(grammar, transform_grammar)

    @staticmethod
    def remove_useless_symbols(grammar: Grammar, transform_grammar=False, *,
                                   perform_unreachable_alg = True,
                                   perform_nongenerating_alg = True) -> Grammar:
        if perform_nongenerating_alg:
            grammar = ContextFree.remove_nongenerating_nonterminals(grammar, transform_grammar=transform_grammar)
            transform_grammar = True
        if perform_unreachable_alg:
            grammar = ContextFree.remove_unreachable_symbols(grammar, transform_grammar=transform_grammar)
        return grammar

    @staticmethod
    def remove_rules_with_epsilon(grammar: Grammar, transform_grammar=False) -> Grammar:
        return remove_rules_with_epsilon(grammar, transform_grammar=transform_grammar)

    @staticmethod
    def find_nonterminals_rewritable_to_epsilon(grammar: Grammar) -> List[Nonterminal]:
        return find_nonterminals_rewritable_to_epsilon(grammar)

    @staticmethod
    def find_nonterminals_reachable_by_unit_rules(grammar: Grammar) -> UnitSymbolRechablingResults:
        return find_nonterminals_reachable_by_unit_rules(grammar)

    @staticmethod
    def remove_unit_rules(grammar: Grammar, transform_grammar=False) -> Grammar:
        return remove_unit_rules(grammar, transform_grammar=transform_grammar)

    @staticmethod
    def transform_to_chomsky_normal_form(grammar: Grammar, transform_grammar=False) -> Grammar:
        return transform_to_chomsky_normal_form(grammar, transform_grammar=transform_grammar)