#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 28.08.2017 10:19
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import *


class ChomskyNonterminal(Nonterminal): pass
class ChomskyGroupNonterminal(ChomskyNonterminal):
    group = []
class ChomskyTermNonterminal(ChomskyNonterminal):
    rewrite_to = None
class ChomskyRule(Rule): pass
class ChomskySplitRule(ChomskyRule):
    from_rule = None
class ChomskyTermRule(ChomskyRule): pass

def transform_to_chomsky_normal_form(grammar: Grammar, transform_grammar=False):
    raise NotImplementedError()