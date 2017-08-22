#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 22:16
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import main, TestCase
from grammpy import *
from grammpy_transforms import ContextFree


class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class C(Nonterminal): pass
class D(Nonterminal): pass
class E(Nonterminal): pass
class Rules(Rule):
    rules = [
        ([S], [A]),
        ([A], [B]),
        ([B], [C]),
        ([C], [A]),
        ([A], [0]),
        ([B], [1]),
        ([C], [2])]

"""
 ---------------------------------
 |   S   |   A   |   B   |   C   |
----------------------------------
S|  []   |  [1]  | [1,2] |[1,2,3]|
----------------------------------
A|       |  []   |  [2]  | [2,3] |
----------------------------------
B|       | [3,4] |  []   |  [3]  |
----------------------------------
C|       |  [4]  | [4,2] |  []   |
----------------------------------
"""

class ResultsInvalidParamsTest(TestCase):
    def test_reachInvalid(self):
        g = Grammar(terminals=[0, 1, 2],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        res = ContextFree.find_nonterminals_reachable_by_unit_rules(g)
        self.assertFalse(res.reach(D, S))
        self.assertFalse(res.reach(S, D))
        self.assertFalse(res.reach(D, D))
        self.assertFalse(res.reach(D, E))

    def test_reachablesInvalid(self):
        g = Grammar(terminals=[0, 1, 2],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        res = ContextFree.find_nonterminals_reachable_by_unit_rules(g)
        self.assertEqual(res.reachables(D), [])
        self.assertEqual(res.reachables(E), [])

    def test_pathRulesInvalid(self):
        g = Grammar(terminals=[0, 1, 2],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        res = ContextFree.find_nonterminals_reachable_by_unit_rules(g)
        self.assertIsNone(res.path_rules(A, D))
        self.assertIsNone(res.path_rules(D, S))
        self.assertIsNone(res.path_rules(D, S))
        self.assertIsNone(res.path_rules(E, D))

