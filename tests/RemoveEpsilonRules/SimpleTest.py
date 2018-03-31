#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 16:01
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import ContextFree
from inspect import isclass

class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class C(Nonterminal): pass
class Rules(Rule):
    rules = [
        ([S], [1, B]),
        ([A], [1, B]),
        ([A], [EPS]),
        ([B], [EPS]),
        ([B], [1, C]),
        ([C], [1, 1])]

"""
S->1B   A->1B   A->eps  B->eps  B->1C   C->11
ToEpsilon: A,B
S->1B   A->1B   A->eps  B->eps  B->1C   C->11   S->1    A->1
                ------  ------                  ++++    ++++
"""


class SimpleTest(TestCase):
    def test_simpleTest(self):
        g = Grammar(terminals=[1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules])
        com = ContextFree.remove_rules_with_epsilon(g)
        self.assertEqual(com.rules_count(), 6)
        class RuleNewS(Rule): rule=([S], [1])
        class RuleNewA(Rule): rule=([A], [1])
        self.assertTrue(com.have_rule(RuleNewS))
        self.assertTrue(com.have_rule(RuleNewA))
        fromS = com.get_rule(RuleNewS)
        self.assertEqual(fromS.fromSymbol, S)
        self.assertEqual(fromS.toSymbol, 1)
        self.assertTrue(isclass(fromS))
        self.assertTrue(issubclass(fromS, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromS.from_rule.rule, ([S], [1, B]))
        self.assertEqual(fromS.replace_index, 1)
        fromA = com.get_rule(RuleNewA)
        self.assertEqual(fromA.fromSymbol, A)
        self.assertEqual(fromA.toSymbol, 1)
        self.assertTrue(isclass(fromA))
        self.assertTrue(issubclass(fromA, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromA.from_rule.rule, ([A], [1, B]))
        self.assertEqual(fromA.replace_index, 1)
        class OldA(Rule): rule=([A], [EPS])
        class OldB(Rule): rule=([B], [EPS])
        self.assertFalse(com.have_rule(OldA))
        self.assertFalse(com.have_rule(OldB))

    def test_simpleTestShouldNotChange(self):
        g = Grammar(terminals=[1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules])
        ContextFree.remove_rules_with_epsilon(g)
        self.assertEqual(g.rules_count(), 6)
        class RuleNewS(Rule): rule=([S], [1])
        class RuleNewA(Rule): rule=([A], [1])
        self.assertFalse(g.have_rule(RuleNewS))
        self.assertFalse(g.have_rule(RuleNewA))
        class OldA(Rule): rule=([A], [EPS])
        class OldB(Rule): rule=([B], [EPS])
        self.assertTrue(g.have_rule(OldA))
        self.assertTrue(g.have_rule(OldB))

    def test_simpleTestShouldChange(self):
        g = Grammar(terminals=[1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_rules_with_epsilon(g, transform_grammar=True)
        self.assertEqual(g.rules_count(), 6)
        class RuleNewS(Rule): rule=([S], [1])
        class RuleNewA(Rule): rule=([A], [1])
        self.assertTrue(g.have_rule(RuleNewS))
        self.assertTrue(g.have_rule(RuleNewA))
        fromS = g.get_rule(RuleNewS)
        self.assertEqual(fromS.fromSymbol, S)
        self.assertEqual(fromS.toSymbol, 1)
        self.assertTrue(isclass(fromS))
        self.assertTrue(issubclass(fromS, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromS.from_rule.rule, ([S], [1, B]))
        self.assertEqual(fromS.replace_index, 1)
        fromA = g.get_rule(RuleNewA)
        self.assertEqual(fromA.fromSymbol, A)
        self.assertEqual(fromA.toSymbol, 1)
        self.assertTrue(isclass(fromA))
        self.assertTrue(issubclass(fromA, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromA.from_rule.rule, ([A], [1, B]))
        self.assertEqual(fromA.replace_index, 1)
        class OldA(Rule): rule=([A], [EPS])
        class OldB(Rule): rule=([B], [EPS])
        self.assertFalse(g.have_rule(OldA))
        self.assertFalse(g.have_rule(OldB))



if __name__ == '__main__':
    main()
