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

    @staticmethod
    def is_grammar_generating(grammar: Grammar):
        g = ContextFree.remove_nongenerating_symbols(grammar)
        return g.start_get() in g.nonterms()
