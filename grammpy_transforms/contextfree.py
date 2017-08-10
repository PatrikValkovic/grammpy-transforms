#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.06.2017 16:39
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Grammar
from .NongeneratingSymbolsRemove import remove_nongenerating_symbol


class ContextFree():
    @staticmethod
    def remove_nongenerastingSymbols(grammar: Grammar, transform_grammar=False):
        return remove_nongenerating_symbol(grammar, transform_grammar)
