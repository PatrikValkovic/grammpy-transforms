#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 21:28
:Licence GNUv3
Part of grammpy-transforms

"""

from inspect import isclass
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

S->A  A->B  B->C  C->A  A->0  B->1  C->2
----  ----  ----  ----

S->A->0
S->A->B->1
S->A->B->C->2
A->B->1
A->B->C->2
B->C->2
B->C->A->0
C->A->0
C->A->B->1
"""

class SimpleTest(TestCase):
    def test_simpleTest(self):
        g = Grammar(terminals=[0, 1, 2],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        com = ContextFree.remove_unit_rules(g)
        # Removed
        class RuleStoA(Rule): rule = ([S], [A])
        self.assertFalse(com.have_rule(RuleStoA))
        class RuleAtoB(Rule): rule = ([A], [B])
        self.assertFalse(com.have_rule(RuleAtoB))
        class RuleBtoC(Rule): rule = ([B], [C])
        self.assertFalse(com.have_rule(RuleBtoC))
        class RuleCtoA(Rule): rule = ([C], [A])
        self.assertFalse(com.have_rule(RuleCtoA))
        # Old rules
        class RuleNewAto0(Rule): rule = ([A], [0])
        self.assertTrue(com.have_rule(RuleNewAto0))
        class RuleNewBto1(Rule): rule = ([B], [1])
        self.assertTrue(com.have_rule(RuleNewBto1))
        class RuleNewCto2(Rule): rule = ([C], [2])
        self.assertTrue(com.have_rule(RuleNewCto2))
        # New rules
        class RuleNewSto0(Rule): rule = ([S], [0])
        self.assertTrue(com.have_rule(RuleNewSto0))
        fromSto0 = com.get_rule(RuleNewSto0)
        self.assertTrue(isclass(fromSto0))
        self.assertTrue(issubclass(fromSto0, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto0.by_rules), 1)
        self.assertEqual(fromSto0.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto0.end_rule.rule, ([A], [0]))
        class RuleNewSto1(Rule): rule = ([S], [1])
        self.assertTrue(com.have_rule(RuleNewSto1))
        fromSto1 = com.get_rule(RuleNewSto1)
        self.assertTrue(isclass(fromSto1))
        self.assertTrue(issubclass(fromSto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1.by_rules), 2)
        self.assertEqual(fromSto1.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromSto1.end_rule.rule, ([B], [1]))
        class RuleNewSto2(Rule): rule = ([S], [2])
        self.assertTrue(com.have_rule(RuleNewSto2))
        fromSto2 = com.get_rule(RuleNewSto2)
        self.assertTrue(isclass(fromSto2))
        self.assertTrue(issubclass(fromSto2, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto2.by_rules), 3)
        self.assertEqual(fromSto2.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto2.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromSto2.by_rules[2].rule, ([B], [C]))
        self.assertEqual(fromSto2.end_rule.rule, ([C], [2]))
        class RuleNewAto1(Rule): rule = ([A], [1])
        self.assertTrue(com.have_rule(RuleNewAto1))
        fromAto1 = com.get_rule(RuleNewAto1)
        self.assertTrue(isclass(fromAto1))
        self.assertTrue(issubclass(fromAto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto1.by_rules), 1)
        self.assertEqual(fromAto1.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAto1.end_rule.rule, ([B], [1]))
        class RuleNewAto2(Rule): rule = ([A], [2])
        self.assertTrue(com.have_rule(RuleNewAto2))
        fromAto2 = com.get_rule(RuleNewAto2)
        self.assertTrue(isclass(fromAto2))
        self.assertTrue(issubclass(fromAto2, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto2.by_rules), 2)
        self.assertEqual(fromAto2.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAto2.by_rules[1].rule, ([B], [C]))
        self.assertEqual(fromAto2.end_rule.rule, ([C], [2]))
        class RuleNewBto2(Rule): rule = ([B], [2])
        self.assertTrue(com.have_rule(RuleNewBto2))
        fromBto2 = com.get_rule(RuleNewBto2)
        self.assertTrue(isclass(fromBto2))
        self.assertTrue(issubclass(fromBto2, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto2.by_rules), 1)
        self.assertEqual(fromBto2.by_rules[0].rule, ([B], [C]))
        self.assertEqual(fromBto2.end_rule.rule, ([C], [2]))
        class RuleNewBto0(Rule): rule = ([B], [0])
        self.assertTrue(com.have_rule(RuleNewBto0))
        fromBto0 = com.get_rule(RuleNewBto0)
        self.assertTrue(isclass(fromBto0))
        self.assertTrue(issubclass(fromBto0, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto0.by_rules), 2)
        self.assertEqual(fromBto0.by_rules[0].rule, ([B], [C]))
        self.assertEqual(fromBto0.by_rules[1].rule, ([C], [A]))
        self.assertEqual(fromBto0.end_rule.rule, ([A], [0]))
        class RuleNewCto0(Rule): rule = ([C], [0])
        self.assertTrue(com.have_rule(RuleNewCto0))
        fromCto0 = com.get_rule(RuleNewCto0)
        self.assertTrue(isclass(fromCto0))
        self.assertTrue(issubclass(fromCto0, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromCto0.by_rules), 1)
        self.assertEqual(fromCto0.by_rules[0].rule, ([C], [A]))
        self.assertEqual(fromCto0.end_rule.rule, ([A], [0]))
        class RuleNewCto1(Rule): rule = ([C], [1])
        self.assertTrue(com.have_rule(RuleNewCto1))
        fromCto1 = com.get_rule(RuleNewCto1)
        self.assertTrue(isclass(fromCto1))
        self.assertTrue(issubclass(fromCto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromCto1.by_rules), 2)
        self.assertEqual(fromCto1.by_rules[0].rule, ([C], [A]))
        self.assertEqual(fromCto1.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromCto1.end_rule.rule, ([B], [1]))

    def test_simpleTestShouldNotChange(self):
        g = Grammar(terminals=[0, 1, 2],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_unit_rules(g)
        # Removed
        class RuleStoA(Rule): rule = ([S], [A])
        self.assertTrue(g.have_rule(RuleStoA))
        class RuleAtoB(Rule): rule = ([A], [B])
        self.assertTrue(g.have_rule(RuleAtoB))
        class RuleBtoC(Rule): rule = ([B], [C])
        self.assertTrue(g.have_rule(RuleBtoC))
        class RuleCtoA(Rule): rule = ([C], [A])
        self.assertTrue(g.have_rule(RuleCtoA))
        # Old rules
        class RuleNewAto0(Rule): rule = ([A], [0])
        self.assertTrue(g.have_rule(RuleNewAto0))
        class RuleNewBto1(Rule): rule = ([B], [1])
        self.assertTrue(g.have_rule(RuleNewBto1))
        class RuleNewCto2(Rule): rule = ([C], [2])
        self.assertTrue(g.have_rule(RuleNewCto2))
        # New rules
        class RuleNewSto0(Rule): rule = ([S], [0])
        self.assertFalse(g.have_rule(RuleNewSto0))
        class RuleNewSto1(Rule): rule = ([S], [1])
        self.assertFalse(g.have_rule(RuleNewSto1))
        class RuleNewSto2(Rule): rule = ([S], [2])
        self.assertFalse(g.have_rule(RuleNewSto2))
        class RuleNewAto1(Rule): rule = ([A], [1])
        self.assertFalse(g.have_rule(RuleNewAto1))
        class RuleNewAto2(Rule): rule = ([A], [2])
        self.assertFalse(g.have_rule(RuleNewAto2))
        class RuleNewBto2(Rule): rule = ([B], [2])
        self.assertFalse(g.have_rule(RuleNewBto2))
        class RuleNewBto0(Rule): rule = ([B], [0])
        self.assertFalse(g.have_rule(RuleNewBto0))
        class RuleNewCto0(Rule): rule = ([C], [0])
        self.assertFalse(g.have_rule(RuleNewCto0))
        class RuleNewCto1(Rule): rule = ([C], [1])
        self.assertFalse(g.have_rule(RuleNewCto1))

    def test_simpleTestShouldChange(self):
        g = Grammar(terminals=[0, 1, 2],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_unit_rules(g, transform_grammar=True)
        # Removed
        class RuleStoA(Rule): rule = ([S], [A])
        self.assertFalse(g.have_rule(RuleStoA))
        class RuleAtoB(Rule): rule = ([A], [B])
        self.assertFalse(g.have_rule(RuleAtoB))
        class RuleBtoC(Rule): rule = ([B], [C])
        self.assertFalse(g.have_rule(RuleBtoC))
        class RuleCtoA(Rule): rule = ([C], [A])
        self.assertFalse(g.have_rule(RuleCtoA))
        # Old rules
        class RuleNewAto0(Rule): rule = ([A], [0])
        self.assertTrue(g.have_rule(RuleNewAto0))
        class RuleNewBto1(Rule): rule = ([B], [1])
        self.assertTrue(g.have_rule(RuleNewBto1))
        class RuleNewCto2(Rule): rule = ([C], [2])
        self.assertTrue(g.have_rule(RuleNewCto2))
        # New rules
        class RuleNewSto0(Rule): rule = ([S], [0])
        self.assertTrue(g.have_rule(RuleNewSto0))
        fromSto0 = g.get_rule(RuleNewSto0)
        self.assertTrue(isclass(fromSto0))
        self.assertTrue(issubclass(fromSto0, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto0.by_rules), 1)
        self.assertEqual(fromSto0.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto0.end_rule.rule, ([A], [0]))
        class RuleNewSto1(Rule): rule = ([S], [1])
        self.assertTrue(g.have_rule(RuleNewSto1))
        fromSto1 = g.get_rule(RuleNewSto1)
        self.assertTrue(isclass(fromSto1))
        self.assertTrue(issubclass(fromSto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1.by_rules), 2)
        self.assertEqual(fromSto1.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromSto1.end_rule.rule, ([B], [1]))
        class RuleNewSto2(Rule): rule = ([S], [2])
        self.assertTrue(g.have_rule(RuleNewSto2))
        fromSto2 = g.get_rule(RuleNewSto2)
        self.assertTrue(isclass(fromSto2))
        self.assertTrue(issubclass(fromSto2, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto2.by_rules), 3)
        self.assertEqual(fromSto2.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto2.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromSto2.by_rules[2].rule, ([B], [C]))
        self.assertEqual(fromSto2.end_rule.rule, ([C], [2]))
        class RuleNewAto1(Rule): rule = ([A], [1])
        self.assertTrue(g.have_rule(RuleNewAto1))
        fromAto1 = g.get_rule(RuleNewAto1)
        self.assertTrue(isclass(fromAto1))
        self.assertTrue(issubclass(fromAto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto1.by_rules), 1)
        self.assertEqual(fromAto1.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAto1.end_rule.rule, ([B], [1]))
        class RuleNewAto2(Rule): rule = ([A], [2])
        self.assertTrue(g.have_rule(RuleNewAto2))
        fromAto2 = g.get_rule(RuleNewAto2)
        self.assertTrue(isclass(fromAto2))
        self.assertTrue(issubclass(fromAto2, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto2.by_rules), 2)
        self.assertEqual(fromAto2.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAto2.by_rules[1].rule, ([B], [C]))
        self.assertEqual(fromAto2.end_rule.rule, ([C], [2]))
        class RuleNewBto2(Rule): rule = ([B], [2])
        self.assertTrue(g.have_rule(RuleNewBto2))
        fromBto2 = g.get_rule(RuleNewBto2)
        self.assertTrue(isclass(fromBto2))
        self.assertTrue(issubclass(fromBto2, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto2.by_rules), 1)
        self.assertEqual(fromBto2.by_rules[0].rule, ([B], [C]))
        self.assertEqual(fromBto2.end_rule.rule, ([C], [2]))
        class RuleNewBto0(Rule): rule = ([B], [0])
        self.assertTrue(g.have_rule(RuleNewBto0))
        fromBto0 = g.get_rule(RuleNewBto0)
        self.assertTrue(isclass(fromBto0))
        self.assertTrue(issubclass(fromBto0, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto0.by_rules), 2)
        self.assertEqual(fromBto0.by_rules[0].rule, ([B], [C]))
        self.assertEqual(fromBto0.by_rules[1].rule, ([C], [A]))
        self.assertEqual(fromBto0.end_rule.rule, ([A], [0]))
        class RuleNewCto0(Rule): rule = ([C], [0])
        self.assertTrue(g.have_rule(RuleNewCto0))
        fromCto0 = g.get_rule(RuleNewCto0)
        self.assertTrue(isclass(fromCto0))
        self.assertTrue(issubclass(fromCto0, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromCto0.by_rules), 1)
        self.assertEqual(fromCto0.by_rules[0].rule, ([C], [A]))
        self.assertEqual(fromCto0.end_rule.rule, ([A], [0]))
        class RuleNewCto1(Rule): rule = ([C], [1])
        self.assertTrue(g.have_rule(RuleNewCto1))
        fromCto1 = g.get_rule(RuleNewCto1)
        self.assertTrue(isclass(fromCto1))
        self.assertTrue(issubclass(fromCto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromCto1.by_rules), 2)
        self.assertEqual(fromCto1.by_rules[0].rule, ([C], [A]))
        self.assertEqual(fromCto1.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromCto1.end_rule.rule, ([B], [1]))
