#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 28.08.2017 10:19
:Licence GNUv3
Part of grammpy-transforms

"""

from copy import copy
from grammpy import *


class ChomskyNonterminal(Nonterminal): pass
class ChomskyGroupNonterminal(ChomskyNonterminal):
    group = []
class ChomskyTermNonterminal(ChomskyNonterminal): pass
class ChomskyRule(Rule): pass
class ChomskySplitRule(ChomskyRule):
    from_rule = None
class ChomskyTermRule(ChomskyRule): pass



def transform_to_chomsky_normal_form(grammar: Grammar, transform_grammar=False):
    # Copy if required
    if transform_grammar is False: grammar = copy(grammar)
    raise NotImplementedError()