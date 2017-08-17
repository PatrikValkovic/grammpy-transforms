#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.06.2017 16:39
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import Grammar
from .NongeneratingSymbolsRemove import remove_nongenerating_symbols
from .UnreachableSymbolsRemove import remove_unreachable_symbols


class ContextFree:
    @staticmethod
    def remove_nongenerating_symbols(grammar: Grammar, transform_grammar=False):
        return remove_nongenerating_symbols(grammar, transform_grammar)

    @staticmethod
    def is_grammar_generating(grammar: Grammar, tranform_gramar=False, perform_remove=True):
        g = grammar
        if perform_remove:
            g = ContextFree.remove_nongenerating_symbols(grammar, transform_grammar=tranform_gramar)
        return g.start_get() in g.nonterms()

    @staticmethod
    def remove_unreachable_symbols(grammar: Grammar, transform_grammar=False):
        return remove_unreachable_symbols(grammar, transform_grammar)
