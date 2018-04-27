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
    """
    Class that associate functions transforming context-free grammars.
    """

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
        """
        Remove nongenerating symbols from the grammar
        :param grammar: Grammar where to remove nongenerating symbols
        :param transform_grammar: True if transformation should be performed in place, false otherwise.
        False by default.
        :return: Grammar without nongenerating symbols
        """
        return remove_nongenerating_nonterminals(grammar, transform_grammar)

    @staticmethod
    def is_grammar_generating(grammar: Grammar, transform_grammar=False, perform_remove=True):
        """
        Check if is grammar generating
        :param grammar: Grammar to check
        :param transform_grammar: True if transformation should be performed in place, false otherwise.
        False by default.
        :param perform_remove: True if should be removed nongenerating symbols.
        True by default.
        :return: True if is grammar generating, false otherwise.
        """
        g = grammar
        if perform_remove:
            g = ContextFree.remove_nongenerating_nonterminals(grammar, transform_grammar=transform_grammar)
        return g.start_get() in g.nonterms()  # TODO if nil?

    @staticmethod
    def remove_unreachable_symbols(grammar: Grammar, transform_grammar=False):
        """
        Remove unreachable symbols from the gramar
        :param grammar: Grammar where to symbols remove
        :param transform_grammar: True if transformation should be performed in place, false otherwise.
        False by default.
        :return: Grammar without unreachable symbols.
        """
        return remove_unreachable_symbols(grammar, transform_grammar)

    @staticmethod
    def remove_useless_symbols(grammar: Grammar, transform_grammar=False, *,
                                   perform_unreachable_alg = True,
                                   perform_nongenerating_alg = True) -> Grammar:
        """
        Remove useless symbols from the grammar
        :param grammar: Grammar where to symbols remove
        :param transform_grammar: True if transformation should be performed in place, false otherwise.
        False by default.
        :param perform_unreachable_alg: True if should remove unreachable symbols.
        True by default.
        :param perform_nongenerating_alg: True if should remove nongenerating symbols.
        True by default.
        :return: Grammar without useless symbols.
        """
        if perform_nongenerating_alg:
            grammar = ContextFree.remove_nongenerating_nonterminals(grammar, transform_grammar=transform_grammar)
            transform_grammar = True
        if perform_unreachable_alg:
            grammar = ContextFree.remove_unreachable_symbols(grammar, transform_grammar=transform_grammar)
        return grammar

    @staticmethod
    def remove_rules_with_epsilon(grammar: Grammar, transform_grammar=False) -> Grammar:
        """
        Remove epsilon rules.
        :param grammar: Grammar where rules remove
        :param transform_grammar: True if transformation should be performed in place, false otherwise.
        False by default.
        :return: Grammar without epsilon rules.
        """
        return remove_rules_with_epsilon(grammar, transform_grammar=transform_grammar)

    @staticmethod
    def find_nonterminals_rewritable_to_epsilon(grammar: Grammar):
        """
        Get nonterminals rewritable to epsilon.
        :param grammar: Grammar where to search.
        :return: Dictionary, where key is nonterminal rewritable to epsilon and value is rule that is responsible for it.
        """
        return find_nonterminals_rewritable_to_epsilon(grammar)

    @staticmethod
    def find_nonterminals_reachable_by_unit_rules(grammar: Grammar) -> UnitSymbolRechablingResults:
        """
        Get nonterminal for which exist unit rule
        :param grammar: Grammar where to search
        :return: Instance of UnitSymbolRechablingResults.
        """
        return find_nonterminals_reachable_by_unit_rules(grammar)

    @staticmethod
    def remove_unit_rules(grammar: Grammar, transform_grammar=False) -> Grammar:
        """
        Remove unit rules from the grammar
        :param grammar: Grammar where the rules remove
        :param transform_grammar: True if transformation should be performed in place, false otherwise.
        False by default.
        :return: Grammar without unit rules.
        """
        return remove_unit_rules(grammar, transform_grammar=transform_grammar)

    @staticmethod
    def transform_to_chomsky_normal_form(grammar: Grammar, transform_grammar=False) -> Grammar:
        """
        Transform grammar to Chomsky Normal Form
        :param grammar: Grammar to transform
        :param transform_grammar: True if transformation should be performed in place, false otherwise.
        False by default.
        :return: Grammar in Chomsky Normal Form.
        """
        return transform_to_chomsky_normal_form(grammar, transform_grammar=transform_grammar)
