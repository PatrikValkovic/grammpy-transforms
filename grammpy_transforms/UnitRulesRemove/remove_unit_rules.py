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
    by_rules = []  # type: List[type]
    end_rule = None  # type: Rule


def _is_unit(rule):
    return len(rule.left) == 1 and len(rule.right) == 1 and \
           isclass(rule.fromSymbol) and isclass(rule.toSymbol) and \
           issubclass(rule.fromSymbol, Nonterminal) and issubclass(rule.toSymbol, Nonterminal)


def _create_rule(path, rule):
    created = type("Reduced" + rule.__name__, (ReducedUnitRule,), ReducedUnitRule.__dict__.copy())
    created.rule = ([path[0].fromSymbol], rule.right)
    created.end_rule = rule
    created.by_rules = path
    return created


def remove_unit_rules(grammar, transform_grammar=False):
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
