#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 11:39
:Licence GNUv3
Part of grammpy-transforms

"""

from inspect import isclass
from typing import List, Dict, Optional
from grammpy import Grammar, Nonterminal, Rule


class UnitSymbolRechablingResults:
    """
    Class containing info about unit rules.
    """
    def __init__(self, field, translation):
        """
        Create isntance of UnitSymbolRechablingResults
        :param field: Result of Floyd-Warshall algorithm
        :param translation: Dictionary where keys is nonterminal and value is position in the field
        """
        self.f = field  # type: List[List[List[Rule] | None]]
        self.t = translation  # type: Dict[Nonterminal, int]

    def reach(self, from_symbol: Nonterminal, to_symbol: Nonterminal) -> bool:
        """
        Check if exists sequence of unit rules between two symbols
        :param from_symbol: From which symbol find
        :param to_symbol:  To which symbol find
        :return: True if exists sequence of unit rules, false otherwise
        """
        if from_symbol not in self.t or to_symbol not in self.t:
            return False
        return self.f[self.t[from_symbol]][self.t[to_symbol]] is not None

    def reachables(self, from_symbol: Nonterminal) -> List[Nonterminal]:
        """
        Get list of nonterminals, what are rewritable from nonterminal passed as parameter by sequence of unit rules.
        :param from_symbol: From which symbol to search
        :return: List of nonterminals
        """
        if from_symbol not in self.t:
            return []
        reachable = []
        index = self.t[from_symbol]
        for n, i in self.t.items():
            if self.f[index][i] is not None:
                reachable.append(n)
        return reachable

    def path_rules(self, from_symbol: Nonterminal, to_symbol: Nonterminal):
        """
        Get sequence of unit rules between first and second parameter
        :param from_symbol: From which symbol
        :param to_symbol: To which symbol
        :return: Sequence of unit rules
        """
        if from_symbol not in self.t or to_symbol not in self.t:
            return None
        return self.f[self.t[from_symbol]][self.t[to_symbol]]


def find_nonterminals_reachable_by_unit_rules(grammar: Grammar) -> UnitSymbolRechablingResults:
    """
    Get nonterminal for which exist unit rule
    :param grammar: Grammar where to search
    :return: Instance of UnitSymbolRechablingResults.
    """
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


