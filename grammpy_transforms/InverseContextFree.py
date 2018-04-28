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
    """
    Class that associate functions transforming Context-Free AST.
    """

    @staticmethod
    def unit_rules_restore(root: Nonterminal) -> Nonterminal:
        """
        Transform rules created by removing unit rules to original rules used in grammar.
        :param root: Root of AST
        :return: Modified AST
        """
        return unit_rules_restore(root)

    @staticmethod
    def epsilon_rules_restore(root: Nonterminal) -> Nonterminal:
        """
        Transform rules created by removing epsilon rules to original rules used in grammar.
        :param root: Root of AST
        :return: Modified AST
        """
        return epsilon_rules_restore(root)

    @staticmethod
    def transform_from_chomsky_normal_form(root: Nonterminal) -> Nonterminal:
        """
        Transform rules created by Chomsky Normal Form to original rules used in grammar.
        :param root: Root of AST
        :return: Modified AST
        """
        return transform_from_chomsky_normal_form(root)
