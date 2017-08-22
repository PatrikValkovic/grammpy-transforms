#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 21:28
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

class SimpleTest(TestCase):
    def test_simpleTest(self):
        g = Grammar(terminals=[0, 1, 2],
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
        self.assertFalse(res.reach(B, S))
        self.assertTrue(res.reach(B, A))
        self.assertTrue(res.reach(B, B))
        self.assertTrue(res.reach(B, C))
        # From B
        self.assertFalse(res.reach(B, S))
        self.assertTrue(res.reach(B, A))
        self.assertTrue(res.reach(B, B))
        self.assertTrue(res.reach(B, C))
        # From C
        self.assertFalse(res.reach(C, S))
        self.assertTrue(res.reach(C, A))
        self.assertTrue(res.reach(C, B))
        self.assertTrue(res.reach(C, C))
        # Reachables
        self.assertEqual(len(res.reachables(S)), 4)
        for n in [S, A, B, C]:
            self.assertIn(n, res.reachables(S))
        self.assertEqual(len(res.reachables(A)), 3)
        for n in [A, B, C]:
            self.assertIn(n, res.reachables(A))
        self.assertEqual(len(res.reachables(B)), 3)
        for n in [A, B, C]:
            self.assertIn(n, res.reachables(B))
        self.assertEqual(len(res.reachables(C)), 3)
        for n in [A, B, C]:
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
        BARules = res.path_rules(B, A)
        self.assertEqual(len(BARules), 2)
        self.assertEqual(BARules[0].rule, ([B], [C]))
        self.assertEqual(BARules[1].rule, ([C], [A]))
        # Rules C
        self.assertEqual(res.path_rules(C, C), [])
        CARules = res.path_rules(C, A)
        self.assertEqual(len(CARules), 1)
        self.assertEqual(CARules[0].rule, ([C], [A]))
        CBRules = res.path_rules(C, B)
        self.assertEqual(len(CBRules), 2)
        self.assertEqual(CBRules[0].rule, ([C], [A]))
        self.assertEqual(CBRules[1].rule, ([A], [B]))
