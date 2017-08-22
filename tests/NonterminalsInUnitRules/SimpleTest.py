#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 20:51
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
class Rules(Rule):
    rules=[
        ([S], [A]),
        ([S], [B]),
        ([A], [C]),
        ([A], [0, A]),
        ([A], [1, S]),
        ([B], [D]),
        ([B], [2, B]),
        ([B], [3, S]),
        ([C], [1, C]),
        ([C], [0]),
        ([D], [3, D]),
        ([D], [2])]

"""
 -------------------------------
 |  S  |  A  |  B  |  C  |  D  |
--------------------------------
S| []  | [1] | [2] |[1,3]|[2,6]|
--------------------------------
A|     | []  |     | [3] |     |
--------------------------------
B|     |     | []  |     | [6] |
--------------------------------
C|     |     |     | []  |     |
--------------------------------
D|     |     |     |     | []  |
--------------------------------

"""


class SimpleTest(TestCase):
    def test_simpleTest(self):
        g = Grammar(terminals=[0,1,2,3],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        res = ContextFree.find_nonterminals_reachable_by_unit_rules(g)
        # From S
        self.assertTrue(res.reach(S, S))
        self.assertTrue(res.reach(S, A))
        self.assertTrue(res.reach(S, B))
        self.assertTrue(res.reach(S, C))
        self.assertTrue(res.reach(S, D))
        # From A
        self.assertFalse(res.reach(A, S))
        self.assertTrue(res.reach(A, A))
        self.assertFalse(res.reach(A, B))
        self.assertTrue(res.reach(A, C))
        self.assertFalse(res.reach(A, D))
        # From B
        self.assertFalse(res.reach(B, S))
        self.assertFalse(res.reach(B, A))
        self.assertTrue(res.reach(B, B))
        self.assertFalse(res.reach(B, C))
        self.assertTrue(res.reach(B, D))
        # From C
        self.assertFalse(res.reach(C, S))
        self.assertFalse(res.reach(C, A))
        self.assertFalse(res.reach(C, B))
        self.assertTrue(res.reach(C, C))
        self.assertFalse(res.reach(C, D))
        # From D
        self.assertFalse(res.reach(D, S))
        self.assertFalse(res.reach(D, A))
        self.assertFalse(res.reach(D, B))
        self.assertFalse(res.reach(D, C))
        self.assertTrue(res.reach(D, D))
        # Reachables
        self.assertEqual(len(res.reachables(S)), 5)
        for n in [S, A, B, C, D]:
            self.assertIn(n, res.reachables(S))
        self.assertEqual(len(res.reachables(A)), 2)
        for n in [A, C]:
            self.assertIn(n, res.reachables(A))
        self.assertEqual(len(res.reachables(B)), 2)
        for n in [B, D]:
            self.assertIn(n, res.reachables(B))
        self.assertEqual(len(res.reachables(C)), 1)
        for n in [C]:
            self.assertIn(n, res.reachables(C))
        self.assertEqual(len(res.reachables(D)), 1)
        for n in [D]:
            self.assertIn(n, res.reachables(D))
        # Rules S
        self.assertEqual(res.path_rules(S, S), [])
        SARules = res.path_rules(S, A)
        self.assertEqual(len(SARules), 1)
        self.assertEqual(SARules[0].rule, ([S], [A]))
        SBRules = res.path_rules(S, B)
        self.assertEqual(len(SBRules), 1)
        self.assertEqual(SBRules[0].rule, ([S], [B]))
        SCRules = res.path_rules(S, C)
        self.assertEqual(len(SCRules), 2)
        self.assertEqual(SCRules[0].rule, ([S], [A]))
        self.assertEqual(SCRules[1].rule, ([A], [C]))
        SDRules = res.path_rules(S, D)
        self.assertEqual(len(SDRules), 2)
        self.assertEqual(SDRules[0].rule, ([S], [B]))
        self.assertEqual(SDRules[1].rule, ([B], [D]))
        # Rules A
        self.assertEqual(res.path_rules(A, A), [])
        ACRules = res.path_rules(A, C)
        self.assertEqual(len(ACRules), 1)
        self.assertEqual(ACRules[0].rule, ([A], [C]))
        # Rules B
        self.assertEqual(res.path_rules(B, B), [])
        BDRules = res.path_rules(B, D)
        self.assertEqual(len(BDRules), 1)
        self.assertEqual(BDRules[0].rule, ([B], [D]))
        # Rules C
        self.assertEqual(res.path_rules(C, C), [])
        # Rules D
        self.assertEqual(res.path_rules(D, D), [])


if __name__ == '__main__':
    main()
