#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 21:14
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
class Rules(Rule):
    rules = [
        ([S], [0, B, 0]),
        ([S], [A]),
        ([A], [0, A]),
        ([A], [B]),
        ([B], [1, B]),
        ([B], [A, B]),
        ([B], [C]),
        ([B], [EPS]),
        ([C], [1, A]),
        ([C], [1])]

"""
 ---------------------------------
 |   S   |   A   |   B   |   C   |
----------------------------------
S|  []   |  [2]  | [2,4] |[2,4,7]|
----------------------------------
A|       |  []   |  [4]  | [4,7] |
----------------------------------
B|       |       |  []   |  [7]  |
----------------------------------
C|       |       |       |  []   |
----------------------------------
"""

class SimpleTest(TestCase):
    def test_simpleTest(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        res = ContextFree.find_nonterminals_reachable_by_unit_rules(g)
        # From S
        self.assertTrue(res.reach(S, S))
        self.assertTrue(res.reach(S, A))
        self.assertTrue(res.reach(S, B))
        self.assertTrue(res.reach(S, C))
        # From A
        self.assertFalse(res.reach(A, S))
        self.assertTrue(res.reach(A, A))
        self.assertTrue(res.reach(A, B))
        self.assertTrue(res.reach(A, C))
        # From B
        self.assertFalse(res.reach(B, S))
        self.assertFalse(res.reach(B, A))
        self.assertTrue(res.reach(B, B))
        self.assertTrue(res.reach(B, C))
        # From C
        self.assertFalse(res.reach(C, S))
        self.assertFalse(res.reach(C, A))
        self.assertFalse(res.reach(C, B))
        self.assertTrue(res.reach(C, C))
        # Reachables
        self.assertEqual(len(res.reachables(S)), 4)
        for n in [S, A, B, C]:
            self.assertIn(n, res.reachables(S))
        self.assertEqual(len(res.reachables(A)), 3)
        for n in [A, B, C]:
            self.assertIn(n, res.reachables(A))
        self.assertEqual(len(res.reachables(B)), 2)
        for n in [B, C]:
            self.assertIn(n, res.reachables(B))
        self.assertEqual(len(res.reachables(C)), 1)
        for n in [C]:
            self.assertIn(n, res.reachables(C))
        # Rules S
        self.assertEqual(res.path_rules(S, S), [])
        SARules = res.path_rules(S, A)
        self.assertEqual(len(SARules), 1)
        self.assertEqual(SARules[0].rule, ([S], [A]))
        SBRules = res.path_rules(S, B)
        self.assertEqual(len(SBRules), 2)
        self.assertEqual(SBRules[0].rule, ([S], [A]))
        self.assertEqual(SBRules[1].rule, ([A], [B]))
        SCRules = res.path_rules(S, C)
        self.assertEqual(len(SCRules), 3)
        self.assertEqual(SCRules[0].rule, ([S], [A]))
        self.assertEqual(SCRules[1].rule, ([A], [B]))
        self.assertEqual(SCRules[2].rule, ([B], [C]))
        # Rules A
        self.assertEqual(res.path_rules(A, A), [])
        ABRules = res.path_rules(A, B)
        self.assertEqual(len(ABRules), 1)
        self.assertEqual(ABRules[0].rule, ([A], [B]))
        ACRules = res.path_rules(A, C)
        self.assertEqual(len(ACRules), 2)
        self.assertEqual(ACRules[0].rule, ([A], [B]))
        self.assertEqual(ACRules[1].rule, ([B], [C]))
        # Rules B
        self.assertEqual(res.path_rules(B, B), [])
        BCRules = res.path_rules(B, C)
        self.assertEqual(len(BCRules), 1)
        self.assertEqual(BCRules[0].rule, ([B], [C]))
        # Rules C
        self.assertEqual(res.path_rules(C, C), [])


if __name__ == '__main__':
    main()
