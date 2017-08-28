#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 15:48
:Licence GNUv3
Part of grammpy-transforms

"""

from inspect import isclass
from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import ContextFree

class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class C(Nonterminal): pass
class Rules(Rule):
    rules = [
        ([S], [A, B, C]),
        ([A], [0, A]),
        ([A], [EPS]),
        ([B], [A]),
        ([B], [1, 1]),
        ([B], [EPS]),
        ([C], [EPS])]

"""
S->ABC  A->0A   A->eps  B->A    B->11   B->eps  C->eps
ToEpsilon: S,A,B,C
S->ABC  A->0A   A->eps  B->A    B->11   B->eps  C->eps  S->BC   S->AC   S->AB   
                ------                  ------  ------  +++++   +++++   +++++

A->0    S->B    S->C    S->A    S->eps
++++    ++++    ++++    ++++    ++++++
"""


class SimpleChainingTest(TestCase):
    def test_simpleChainingTest(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        com = ContextFree.remove_rules_with_epsilon(g)
        self.assertEqual(len(com.rules()), 12)
        class RuleNewStoBC(Rule): rule=([S], [B, C])
        class RuleNewStoAC(Rule): rule=([S], [A, C])
        class RuleNewStoAB(Rule): rule=([S], [A, B])
        class RuleNewAto0(Rule): rule=([A], [0])
        class RuleNewStoB(Rule): rule=([S], [B])
        class RuleNewStoC(Rule): rule=([S], [C])
        class RuleNewStoA(Rule): rule=([S], [A])
        class RuleNewStoEPS(Rule): rule=([S], [EPS])
        self.assertTrue(com.have_rule([RuleNewStoBC, RuleNewStoAC, RuleNewStoAB, RuleNewAto0,
                                       RuleNewStoB, RuleNewStoC, RuleNewStoA, RuleNewStoEPS]))
        fromStoBC = com.get_rule(RuleNewStoBC)
        self.assertTrue(isclass(fromStoBC))
        self.assertTrue(issubclass(fromStoBC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoBC.from_rule.rule, ([S], [A, B, C]))
        self.assertEqual(fromStoBC.replace_index, 0)
        fromStoAC = com.get_rule(RuleNewStoAC)
        self.assertTrue(isclass(fromStoAC))
        self.assertTrue(issubclass(fromStoAC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoAC.from_rule.rule, ([S], [A, B, C]))
        self.assertEqual(fromStoAC.replace_index, 1)
        fromStoAB = com.get_rule(RuleNewStoAB)
        self.assertTrue(isclass(fromStoAB))
        self.assertTrue(issubclass(fromStoAB, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoAB.from_rule.rule, ([S], [A, B, C]))
        self.assertEqual(fromStoAB.replace_index, 2)
        fromAto0 = com.get_rule(RuleNewAto0)
        self.assertTrue(isclass(fromAto0))
        self.assertTrue(issubclass(fromAto0, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromAto0.from_rule.rule, ([A], [0, A]))
        self.assertEqual(fromAto0.replace_index, 1)
        fromStoA = com.get_rule(RuleNewStoA)
        self.assertTrue(isclass(fromStoA))
        self.assertTrue(issubclass(fromStoA, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoA.from_rule.rule, ([S], [A, C]))
        self.assertEqual(fromStoA.replace_index, 1)
        fromStoB = com.get_rule(RuleNewStoB)
        self.assertTrue(isclass(fromStoB))
        self.assertTrue(issubclass(fromStoB, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoB.from_rule.rule, ([S], [B, C]))
        self.assertEqual(fromStoB.replace_index, 1)
        fromStoC = com.get_rule(RuleNewStoC)
        self.assertTrue(isclass(fromStoC))
        self.assertTrue(issubclass(fromStoC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoC.from_rule.rule, ([S], [B, C]))
        self.assertEqual(fromStoC.replace_index, 0)
        fromStoEPS = com.get_rule(RuleNewStoEPS)
        self.assertTrue(isclass(fromStoEPS))
        self.assertTrue(issubclass(fromStoEPS, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoEPS.from_rule.rule, ([S], [C]))
        self.assertEqual(fromStoEPS.replace_index, 0)
        class RuleOldAtoEps(Rule): rule=([A], [EPS])
        class RuleOldBtoEps(Rule): rule=([B], [EPS])
        class RuleOldCtoEps(Rule): rule=([C], [EPS])
        self.assertFalse(com.have_rule(RuleOldAtoEps))
        self.assertFalse(com.have_rule(RuleOldBtoEps))
        self.assertFalse(com.have_rule(RuleOldCtoEps))

    def test_simpleChainingTestShouldNotChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_rules_with_epsilon(g)
        self.assertEqual(len(g.rules()), 7)
        class RuleNewStoBC(Rule): rule=([S], [B, C])
        class RuleNewStoAC(Rule): rule=([S], [A, C])
        class RuleNewStoAB(Rule): rule=([S], [A, B])
        class RuleNewAto0(Rule): rule=([A], [0])
        class RuleNewStoB(Rule): rule=([S], [B])
        class RuleNewStoC(Rule): rule=([S], [C])
        class RuleNewStoA(Rule): rule=([S], [A])
        class RuleNewStoEPS(Rule): rule=([S], [EPS])
        self.assertFalse(g.have_rule(RuleNewStoBC))
        self.assertFalse(g.have_rule(RuleNewStoAC))
        self.assertFalse(g.have_rule(RuleNewStoAB))
        self.assertFalse(g.have_rule(RuleNewAto0))
        self.assertFalse(g.have_rule(RuleNewStoB))
        self.assertFalse(g.have_rule(RuleNewStoC))
        self.assertFalse(g.have_rule(RuleNewStoA))
        self.assertFalse(g.have_rule(RuleNewStoEPS))
        class RuleOldAtoEps(Rule): rule=([A], [EPS])
        class RuleOldBtoEps(Rule): rule=([B], [EPS])
        class RuleOldCtoEps(Rule): rule=([C], [EPS])
        self.assertTrue(g.have_rule(RuleOldAtoEps))
        self.assertTrue(g.have_rule(RuleOldBtoEps))
        self.assertTrue(g.have_rule(RuleOldCtoEps))

    def test_simpleChainingTestShouldChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_rules_with_epsilon(g, transform_grammar=True)
        self.assertEqual(len(g.rules()), 12)
        class RuleNewStoBC(Rule): rule=([S], [B, C])
        class RuleNewStoAC(Rule): rule=([S], [A, C])
        class RuleNewStoAB(Rule): rule=([S], [A, B])
        class RuleNewAto0(Rule): rule=([A], [0])
        class RuleNewStoB(Rule): rule=([S], [B])
        class RuleNewStoC(Rule): rule=([S], [C])
        class RuleNewStoA(Rule): rule=([S], [A])
        class RuleNewStoEPS(Rule): rule=([S], [EPS])
        self.assertTrue(g.have_rule([RuleNewStoBC, RuleNewStoAC, RuleNewStoAB, RuleNewAto0,
                                       RuleNewStoB, RuleNewStoC, RuleNewStoA, RuleNewStoEPS]))
        fromStoBC = g.get_rule(RuleNewStoBC)
        self.assertTrue(isclass(fromStoBC))
        self.assertTrue(issubclass(fromStoBC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoBC.from_rule.rule, ([S], [A, B, C]))
        self.assertEqual(fromStoBC.replace_index, 0)
        fromStoAC = g.get_rule(RuleNewStoAC)
        self.assertTrue(isclass(fromStoAC))
        self.assertTrue(issubclass(fromStoAC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoAC.from_rule.rule, ([S], [A, B, C]))
        self.assertEqual(fromStoAC.replace_index, 1)
        fromStoAB = g.get_rule(RuleNewStoAB)
        self.assertTrue(isclass(fromStoAB))
        self.assertTrue(issubclass(fromStoAB, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoAB.from_rule.rule, ([S], [A, B, C]))
        self.assertEqual(fromStoAB.replace_index, 2)
        fromAto0 = g.get_rule(RuleNewAto0)
        self.assertTrue(isclass(fromAto0))
        self.assertTrue(issubclass(fromAto0, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromAto0.from_rule.rule, ([A], [0, A]))
        self.assertEqual(fromAto0.replace_index, 1)
        fromStoA = g.get_rule(RuleNewStoA)
        self.assertTrue(isclass(fromStoA))
        self.assertTrue(issubclass(fromStoA, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoA.from_rule.rule, ([S], [A, C]))
        self.assertEqual(fromStoA.replace_index, 1)
        fromStoB = g.get_rule(RuleNewStoB)
        self.assertTrue(isclass(fromStoB))
        self.assertTrue(issubclass(fromStoB, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoB.from_rule.rule, ([S], [B, C]))
        self.assertEqual(fromStoB.replace_index, 1)
        fromStoC = g.get_rule(RuleNewStoC)
        self.assertTrue(isclass(fromStoC))
        self.assertTrue(issubclass(fromStoC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoC.from_rule.rule, ([S], [B, C]))
        self.assertEqual(fromStoC.replace_index, 0)
        fromStoEPS = g.get_rule(RuleNewStoEPS)
        self.assertTrue(isclass(fromStoEPS))
        self.assertTrue(issubclass(fromStoEPS, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoEPS.from_rule.rule, ([S], [C]))
        self.assertEqual(fromStoEPS.replace_index, 0)
        class RuleOldAtoEps(Rule): rule=([A], [EPS])
        class RuleOldBtoEps(Rule): rule=([B], [EPS])
        class RuleOldCtoEps(Rule): rule=([C], [EPS])
        self.assertFalse(g.have_rule(RuleOldAtoEps))
        self.assertFalse(g.have_rule(RuleOldBtoEps))
        self.assertFalse(g.have_rule(RuleOldCtoEps))





if __name__ == '__main__':
    main()
