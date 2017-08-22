#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 11:39
:Licence GNUv3
Part of grammpy-transforms

"""

from typing import List
from grammpy import Nonterminal, Rule


class UnitSymbolRechablingResults:
    def reach(self, from_symbol: Nonterminal, to_symbol: Nonterminal) -> bool:
        raise NotImplementedError()

    def reachables(self, from_symbol: Nonterminal) -> List[Nonterminal]:
        raise NotImplementedError()

    def path_rules(self, from_symbol: Nonterminal, to_symbol: Nonterminal) -> List[Rule]:
        raise NotImplementedError()


def find_nonterminals_reachable_by_unit_rules(grammar) -> UnitSymbolRechablingResults:
    raise NotImplementedError()
