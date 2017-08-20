#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 15:43
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Grammar, Rule


class EpsilonRemovedRule(Rule):
    from_rule = None  # type: Rule
    replace_index = None  # type: int


def remove_rules_with_epsilon(grammar: Grammar, transform_grammar=True) -> Grammar:
    raise NotImplementedError()
