#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 03.09.2017 10:49
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import *
from .UnitRulesRemove import unit_rules_restore
from .EpsilonRulesRemove import epsilon_rules_restore
from .ChomskyForm import transform_from_chomsky_normal_form

__all__ = ['InverseContextFree']


class InverseContextFree:
    @staticmethod
    def unit_rules_restore(root: Nonterminal) -> Nonterminal:
        return unit_rules_restore(root)

    @staticmethod
    def epsilon_rules_restore(root: Nonterminal) -> Nonterminal:
        return epsilon_rules_restore(root)

    @staticmethod
    def transform_from_chomsky_normal_form(root: Nonterminal) -> Nonterminal:
        return transform_from_chomsky_normal_form(root)
