#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 11:37
:Licence GNUv3
Part of grammpy-transforms

"""

from typing import List
from grammpy import *

class ReducedUnitRule(Rule):
    by_rules = []  # type: List[Rule]
    end_rule = None  # type: Rule


def remove_unit_rules(grammar: Grammar, transform_grammar=False) -> Grammar:
    raise NotImplementedError()