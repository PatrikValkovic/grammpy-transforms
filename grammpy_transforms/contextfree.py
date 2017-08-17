#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.06.2017 16:39
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Grammar
from .NongeneratingSymbolsRemove import remove_nongenerating_symbols


class ContextFree():
    @staticmethod
    def remove_nongenerating_symbols(grammar: Grammar, transform_grammar=False):
        return remove_nongenerating_symbols(grammar, transform_grammar)
