#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 16:07
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
        ([S], [0, A]),
        ([S], [1, C]),
        ([S], [C, C]),
        ([A], [B]),
        ([B], [S]),
        ([B], [EPS]),
        ([C], [A]),
        ([C], [S])]

"""
S->0A  S->1C   S->CC  A->B    B->S   B->eps  C->A C->S
ToEpsilon: S,A,B,C
S->0A  S->1C   S->CC  A->B    B->S   B->eps  C->A C->S
                                     ------
                            
S->0   S->1    S->C
               S->EPS
"""


class SimpleChainingTest(TestCase):
    def test_simpleChainingTest(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        com = ContextFree.remove_rules_with_epsilon(g)
        self.assertEqual(len(com.rules()), 11)
        class RuleNewSto0(Rule): rule=([S], [0])
        class RuleNewSto1(Rule): rule=([S], [1])
        class RuleNewStoC(Rule): rule=([S], [C])
        class RuleNewStoEPS(Rule): rule=([S], [EPS])
        self.assertTrue(com.have_rule([RuleNewSto0, RuleNewSto1, RuleNewStoC, RuleNewStoEPS]))
        fromSto0 = com.get_rule(RuleNewSto0)
        self.assertTrue(isclass(fromSto0))
        self.assertTrue(issubclass(fromSto0, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromSto0.from_rule.rule, ([S], [0, A]))
        self.assertEqual(fromSto0.replace_index, 1)
        fromSto1 = com.get_rule(RuleNewSto1)
        self.assertTrue(isclass(fromSto1))
        self.assertTrue(issubclass(fromSto1, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromSto1.from_rule.rule, ([S], [1, C]))
        self.assertEqual(fromSto1.replace_index, 1)
        fromStoC = com.get_rule(RuleNewStoC)
        self.assertTrue(isclass(fromStoC))
        self.assertTrue(issubclass(fromStoC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoC.from_rule.rule, ([S], [C, C]))
        self.assertEqual(fromStoC.replace_index, 0)
        fromStoEPS = com.get_rule(RuleNewStoEPS)
        self.assertTrue(isclass(fromStoEPS))
        self.assertTrue(issubclass(fromStoEPS, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoEPS.from_rule.rule, ([S], [C]))
        self.assertEqual(fromStoEPS.replace_index, 0)
        class RuleOldBtoEps(Rule): rule=([B], [EPS])
        self.assertFalse(com.have_rule(RuleOldBtoEps))

    def test_simpleChainingTestShouldNotChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_rules_with_epsilon(g)
        self.assertEqual(len(g.rules()), 8)
        class RuleNewSto0(Rule): rule=([S], [0])
        class RuleNewSto1(Rule): rule=([S], [1])
        class RuleNewStoC(Rule): rule=([S], [C])
        class RuleNewStoEPS(Rule): rule=([S], [EPS])
        self.assertFalse(g.have_rule(RuleNewSto0))
        self.assertFalse(g.have_rule(RuleNewSto1))
        self.assertFalse(g.have_rule(RuleNewStoC))
        self.assertFalse(g.have_rule(RuleNewStoEPS))
        class RuleOldBtoEps(Rule): rule=([B], [EPS])
        self.assertTrue(g.have_rule(RuleOldBtoEps))

    def test_simpleChainingTestShouldChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_rules_with_epsilon(g, transform_grammar=True)
        self.assertEqual(len(g.rules()), 11)
        class RuleNewSto0(Rule): rule=([S], [0])
        class RuleNewSto1(Rule): rule=([S], [1])
        class RuleNewStoC(Rule): rule=([S], [C])
        class RuleNewStoEPS(Rule): rule=([S], [EPS])
        self.assertTrue(g.have_rule([RuleNewSto0, RuleNewSto1, RuleNewStoC, RuleNewStoEPS]))
        fromSto0 = g.get_rule(RuleNewSto0)
        self.assertTrue(isclass(fromSto0))
        self.assertTrue(issubclass(fromSto0, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromSto0.from_rule.rule, ([S], [0, A]))
        self.assertEqual(fromSto0.replace_index, 1)
        fromSto1 = g.get_rule(RuleNewSto1)
        self.assertTrue(isclass(fromSto1))
        self.assertTrue(issubclass(fromSto1, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromSto1.from_rule.rule, ([S], [1, C]))
        self.assertEqual(fromSto1.replace_index, 1)
        fromStoC = g.get_rule(RuleNewStoC)
        self.assertTrue(isclass(fromStoC))
        self.assertTrue(issubclass(fromStoC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoC.from_rule.rule, ([S], [C, C]))
        self.assertEqual(fromStoC.replace_index, 0)
        fromStoEPS = g.get_rule(RuleNewStoEPS)
        self.assertTrue(isclass(fromStoEPS))
        self.assertTrue(issubclass(fromStoEPS, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoEPS.from_rule.rule, ([S], [C]))
        self.assertEqual(fromStoEPS.replace_index, 0)
        class RuleOldBtoEps(Rule): rule=([B], [EPS])
        self.assertFalse(g.have_rule(RuleOldBtoEps))




if __name__ == '__main__':
    main()
