#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 11:39
:Licence GNUv3
Part of grammpy-transforms

"""

from inspect import isclass
from typing import List
from grammpy import Grammar, Nonterminal, Rule


class UnitSymbolRechablingResults:
    def __init__(self, field, translation):
        raise NotImplementedError()

    def reach(self, from_symbol: Nonterminal, to_symbol: Nonterminal) -> bool:
        raise NotImplementedError()

    def reachables(self, from_symbol: Nonterminal) -> List[Nonterminal]:
        raise NotImplementedError()

    def path_rules(self, from_symbol: Nonterminal, to_symbol: Nonterminal) -> List[Rule]:
        raise NotImplementedError()


def find_nonterminals_reachable_by_unit_rules(grammar: Grammar) -> UnitSymbolRechablingResults:
    # Get nonterms
    nonterms = grammar.nonterms()
    l = len(nonterms)
    # Create indexes for nonterms
    nonterm_to_index = dict()
    for i in range(l):
        nonterm_to_index[nonterms[i]] = i
    # Prepare field
    field = [[None for _ in nonterms] for _ in nonterms]
    # Fill diagonal
    for i in range(l):
        field[i][i] = list()
    # Fill rules
    for rule in grammar.rules():
        if len(rule.left)==1 and len(rule.right)==1 and \
                isclass(rule.fromSymbol) and isclass(rule.toSymbol) and \
                issubclass(rule.fromSymbol, Nonterminal) and issubclass(rule.toSymbol, Nonterminal):
            field[nonterm_to_index[rule.fromSymbol]][nonterm_to_index[rule.toSymbol]] = [rule]
    # Floyd Warshall
    f = field
    for k in range(l):
        for i in range(l):
            for j in range(l):
                if f[i][k] is not None and f[k][j] is not None:
                    if f[i][j] is None or len(f[i][j]) > len(f[i][k]) + len(f[k][j]):
                        f[i][j] = f[i][k] + f[k][j]
    # Return results
    return UnitSymbolRechablingResults(f, nonterm_to_index)


