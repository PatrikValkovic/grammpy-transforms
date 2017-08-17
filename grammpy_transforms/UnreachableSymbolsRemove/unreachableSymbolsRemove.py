#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.06.2017 16:39
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Grammar
from copy import copy


def remove_unreachable_symbols(grammar: Grammar, transform_grammar=False):
    # Copy if required
    if transform_grammar is False: grammar = copy(grammar)
    raise NotImplementedError()