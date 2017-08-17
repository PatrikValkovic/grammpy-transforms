#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 17.08.207 13:29
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Grammar
from copy import copy


def remove_unreachable_symbols(grammar: Grammar, transform_grammar=False) -> Grammar:
    # Copy if required
    if transform_grammar is False: grammar = copy(grammar)
    raise NotImplementedError()