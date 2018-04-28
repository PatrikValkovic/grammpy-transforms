#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 11:37
:Licence GNUv3
Part of grammpy-transforms

"""

from inspect import isclass
from copy import copy
from typing import List
from grammpy import *
from .find_symbols_reachable_by_unit_rules import find_nonterminals_reachable_by_unit_rules


class ReducedUnitRule(Rule):
    """
    Represent rule that replace sequence of unit rules and last not unit rule
    """
    by_rules = []  # type: List[type]
    end_rule = None  # type: Rule


def _is_unit(rule):
    """
    Check if parameter is unit rule
    :param rule: Object to check
    :return: True if is parameter unit rule, false otherwise
    """
    return len(rule.left) == 1 and len(rule.right) == 1 and \
           isclass(rule.fromSymbol) and isclass(rule.toSymbol) and \
           issubclass(rule.fromSymbol, Nonterminal) and issubclass(rule.toSymbol, Nonterminal)


def _create_rule(path, rule):
    """
    Create ReducedUnitRule based on sequence of unit rules and end rule
    :param path: Sequence of unit rules
    :param rule: Rule that is attached after sequence of unit rules
    :return: ReducedUnitRule class
    """
    created = type("Reduced" + rule.__name__, (ReducedUnitRule,), ReducedUnitRule.__dict__.copy())
    created.rule = ([path[0].fromSymbol], rule.right)
    created.end_rule = rule
    created.by_rules = path
    return created


def remove_unit_rules(grammar, transform_grammar=False):
    """
    Remove unit rules from the grammar
    :param grammar: Grammar where the rules remove
    :param transform_grammar: True if transformation should be performed in place, false otherwise.
    False by default.
    :return: Grammar without unit rules.
    """
    if transform_grammar is False: grammar = copy(grammar)
    # get connections
    res = find_nonterminals_reachable_by_unit_rules(grammar)
    # iterate through rules
    for rule in grammar.rules():
        if _is_unit(rule):
            grammar.remove_rule(rule)
            continue
        for nonterm in grammar.nonterms():
            path = res.path_rules(nonterm, rule.fromSymbol)
            if path is not None and len(path) > 0:
                created = _create_rule(path, rule)
                grammar.add_rule(created)
    return grammar
