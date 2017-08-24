#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 21:14
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

S->0B0  S->A  A->0A  A->B  B->1B  B->AB  B->C  B->EPS  C->1A  C->1
        ----         ----                ----              
        
S->A->0A
S->A->B->1B
S->A->B->AB
S->A->B->eps
S->A->B->C->1A
S->A->B->C->1
A->B->1B
A->B->AB
A->B->eps
A->B->C->1A
A->B->C->1    
B->C->1A
B->C->1    
"""

class SimpleTest(TestCase):
    def test_simpleTest(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        com = ContextFree.remove_unit_rules(g)
        # Removed
        class RuleStoA(Rule): rule=([S], [A])
        self.assertFalse(com.have_rule(RuleStoA))
        class RuleAtoB(Rule): rule=([A], [B])
        self.assertFalse(com.have_rule(RuleAtoB))
        class RuleBtoC(Rule): rule=([B], [C])
        self.assertFalse(com.have_rule(RuleBtoC))
        # Old rules
        class RuleNewSto0B0(Rule): rule = ([S], [0, B, 0])
        self.assertTrue(com.have_rule(RuleNewSto0B0))
        class RuleNewAto0A(Rule): rule = ([A], [0, A])
        self.assertTrue(com.have_rule(RuleNewAto0A))
        class RuleNewBto1B(Rule): rule = ([B], [1, B])
        self.assertTrue(com.have_rule(RuleNewBto1B))
        class RuleNewBtoAB(Rule): rule = ([B], [A, B])
        self.assertTrue(com.have_rule(RuleNewBtoAB))
        class RuleNewBtoEPS(Rule): rule = ([B], [EPS])
        self.assertTrue(com.have_rule(RuleNewBtoEPS))
        class RuleNewCto1A(Rule): rule = ([C], [1, A])
        self.assertTrue(com.have_rule(RuleNewCto1A))
        class RuleNewCto1(Rule): rule = ([C], [1])
        self.assertTrue(com.have_rule(RuleNewCto1))
        # New rules
        class RuleNewSto0A(Rule): rule = ([S], [0, A])
        self.assertTrue(com.have_rule(RuleNewSto0A))
        fromSto0A = com.get_rule(RuleNewSto0A)
        self.assertTrue(isclass(fromSto0A))
        self.assertTrue(issubclass(fromSto0A, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto0A.by_rules), 1)
        self.assertEqual(fromSto0A.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto0A.end_rule.rule, ([A], [0, A]))
        class RuleNewSto1B(Rule): rule = ([S], [1, B])
        self.assertTrue(com.have_rule(RuleNewSto1B))
        fromSto1B = com.get_rule(RuleNewSto1B)
        self.assertTrue(isclass(fromSto1B))
        self.assertTrue(issubclass(fromSto1B, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1B.by_rules), 2)
        self.assertEqual(fromSto1B.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1B.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromSto1B.end_rule.rule, ([B], [1, B]))
        class RuleNewStoAB(Rule): rule = ([S], [A, B])
        self.assertTrue(com.have_rule(RuleNewStoAB))
        fromStoAB = com.get_rule(RuleNewStoAB)
        self.assertTrue(isclass(fromStoAB))
        self.assertTrue(issubclass(fromStoAB, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromStoAB.by_rules), 2)
        self.assertEqual(fromStoAB.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromStoAB.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromStoAB.end_rule.rule, ([B], [A, B]))
        class RuleNewStoEPS(Rule): rule = ([S], [EPS])
        self.assertTrue(com.have_rule(RuleNewStoEPS))
        fromStoEPS = com.get_rule(RuleNewStoEPS)
        self.assertTrue(isclass(fromStoEPS))
        self.assertTrue(issubclass(fromStoEPS, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromStoEPS.by_rules), 2)
        self.assertEqual(fromStoEPS.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromStoEPS.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromStoEPS.end_rule.rule, ([B], [EPS]))
        class RuleNewSto1A(Rule): rule = ([S], [1, A])
        self.assertTrue(com.have_rule(RuleNewSto1A))
        fromSto1A = com.get_rule(RuleNewSto1A)
        self.assertTrue(isclass(fromSto1A))
        self.assertTrue(issubclass(fromSto1A, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1A.by_rules), 3)
        self.assertEqual(fromSto1A.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1A.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromSto1A.by_rules[2].rule, ([B], [C]))
        self.assertEqual(fromSto1A.end_rule.rule, ([C], [1, A]))
        class RuleNewSto1(Rule): rule = ([S], [1])
        self.assertTrue(com.have_rule(RuleNewSto1))
        fromSto1 = com.get_rule(RuleNewSto1)
        self.assertTrue(isclass(fromSto1))
        self.assertTrue(issubclass(fromSto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1.by_rules), 3)
        self.assertEqual(fromSto1.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromSto1.by_rules[2].rule, ([B], [C]))
        self.assertEqual(fromSto1.end_rule.rule, ([C], [1]))
        class RuleNewAto1B(Rule): rule = ([A], [1, B])
        self.assertTrue(com.have_rule(RuleNewAto1B))
        fromAto1B = com.get_rule(RuleNewAto1B)
        self.assertTrue(isclass(fromAto1B))
        self.assertTrue(issubclass(fromAto1B, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto1B.by_rules), 1)
        self.assertEqual(fromAto1B.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAto1B.end_rule.rule, ([B], [1, B]))
        class RuleNewAtoAB(Rule): rule = ([A], [A, B])
        self.assertTrue(com.have_rule(RuleNewAtoAB))
        fromAtoAB = com.get_rule(RuleNewAtoAB)
        self.assertTrue(isclass(fromAtoAB))
        self.assertTrue(issubclass(fromAtoAB, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAtoAB.by_rules), 1)
        self.assertEqual(fromAtoAB.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAtoAB.end_rule.rule, ([B], [A, B]))
        class RuleNewAtoEPS(Rule): rule = ([A], [EPS])
        self.assertTrue(com.have_rule(RuleNewAtoEPS))
        fromAtoEPS = com.get_rule(RuleNewAtoEPS)
        self.assertTrue(isclass(fromAtoEPS))
        self.assertTrue(issubclass(fromAtoEPS, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAtoEPS.by_rules), 1)
        self.assertEqual(fromAtoEPS.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAtoEPS.end_rule.rule, ([B], [EPS]))
        class RuleNewAto1A(Rule): rule = ([A], [1, A])
        self.assertTrue(com.have_rule(RuleNewAto1A))
        fromAto1A = com.get_rule(RuleNewAto1A)
        self.assertTrue(isclass(fromAto1A))
        self.assertTrue(issubclass(fromAto1A, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto1A.by_rules), 2)
        self.assertEqual(fromAto1A.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAto1A.by_rules[1].rule, ([B], [C]))
        self.assertEqual(fromAto1A.end_rule.rule, ([C], [1, A]))
        class RuleNewAto1(Rule): rule = ([A], [1])
        self.assertTrue(com.have_rule(RuleNewAto1))
        fromAto1 = com.get_rule(RuleNewAto1)
        self.assertTrue(isclass(fromAto1))
        self.assertTrue(issubclass(fromAto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto1.by_rules), 2)
        self.assertEqual(fromAto1.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAto1.by_rules[1].rule, ([B], [C]))
        self.assertEqual(fromAto1.end_rule.rule, ([C], [1]))
        class RuleNewBto1A(Rule): rule = ([B], [1, A])
        self.assertTrue(com.have_rule(RuleNewBto1A))
        fromBto1A = com.get_rule(RuleNewBto1A)
        self.assertTrue(isclass(fromBto1A))
        self.assertTrue(issubclass(fromBto1A, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto1A.by_rules), 1)
        self.assertEqual(fromBto1A.by_rules[0].rule, ([B], [C]))
        self.assertEqual(fromBto1A.end_rule.rule, ([C], [1, A]))
        class RuleNewBto1(Rule): rule = ([B], [1])
        self.assertTrue(com.have_rule(RuleNewBto1))
        fromBto1 = com.get_rule(RuleNewBto1)
        self.assertTrue(isclass(fromBto1))
        self.assertTrue(issubclass(fromBto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto1.by_rules), 1)
        self.assertEqual(fromBto1.by_rules[0].rule, ([B], [C]))
        self.assertEqual(fromBto1.end_rule.rule, ([C], [1]))

    def test_simpleTestShouldNotChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_unit_rules(g)
        # Removed
        class RuleStoA(Rule): rule=([S], [A])
        self.assertTrue(g.have_rule(RuleStoA))
        class RuleAtoB(Rule): rule=([A], [B])
        self.assertTrue(g.have_rule(RuleAtoB))
        class RuleBtoC(Rule): rule=([B], [C])
        self.assertTrue(g.have_rule(RuleBtoC))
        # Old rules
        class RuleNewSto0B0(Rule): rule = ([S], [0, B, 0])
        self.assertTrue(g.have_rule(RuleNewSto0B0))
        class RuleNewAto0A(Rule): rule = ([A], [0, A])
        self.assertTrue(g.have_rule(RuleNewAto0A))
        class RuleNewBto1B(Rule): rule = ([B], [1, B])
        self.assertTrue(g.have_rule(RuleNewBto1B))
        class RuleNewBtoAB(Rule): rule = ([B], [A, B])
        self.assertTrue(g.have_rule(RuleNewBtoAB))
        class RuleNewBtoEPS(Rule): rule = ([B], [EPS])
        self.assertTrue(g.have_rule(RuleNewBtoEPS))
        class RuleNewCto1A(Rule): rule = ([C], [1, A])
        self.assertTrue(g.have_rule(RuleNewCto1A))
        class RuleNewCto1(Rule): rule = ([C], [1])
        self.assertTrue(g.have_rule(RuleNewCto1))
        # New rules
        class RuleNewSto0A(Rule): rule = ([S], [0, A])
        self.assertFalse(g.have_rule(RuleNewSto0A))
        class RuleNewSto1B(Rule): rule = ([S], [1, B])
        self.assertFalse(g.have_rule(RuleNewSto1B))
        class RuleNewStoAB(Rule): rule = ([S], [A, B])
        self.assertFalse(g.have_rule(RuleNewStoAB))
        class RuleNewStoEPS(Rule): rule = ([S], [EPS])
        self.assertFalse(g.have_rule(RuleNewStoEPS))
        class RuleNewSto1A(Rule): rule = ([S], [1, A])
        self.assertFalse(g.have_rule(RuleNewSto1A))
        class RuleNewSto1(Rule): rule = ([S], [1])
        self.assertFalse(g.have_rule(RuleNewSto1))
        class RuleNewAto1B(Rule): rule = ([A], [1, B])
        self.assertFalse(g.have_rule(RuleNewAto1B))
        class RuleNewAtoAB(Rule): rule = ([A], [A, B])
        self.assertFalse(g.have_rule(RuleNewAtoAB))
        class RuleNewAtoEPS(Rule): rule = ([A], [EPS])
        self.assertFalse(g.have_rule(RuleNewAtoEPS))
        class RuleNewAto1A(Rule): rule = ([A], [1, A])
        self.assertFalse(g.have_rule(RuleNewAto1A))
        class RuleNewAto1(Rule): rule = ([A], [1])
        self.assertFalse(g.have_rule(RuleNewAto1))
        class RuleNewBto1A(Rule): rule = ([B], [1, A])
        self.assertFalse(g.have_rule(RuleNewBto1A))
        class RuleNewBto1(Rule): rule = ([B], [1])
        self.assertFalse(g.have_rule(RuleNewBto1))

    def test_simpleTestShouldChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_unit_rules(g, transform_grammar=True)
        # Removed
        class RuleStoA(Rule): rule=([S], [A])
        self.assertFalse(g.have_rule(RuleStoA))
        class RuleAtoB(Rule): rule=([A], [B])
        self.assertFalse(g.have_rule(RuleAtoB))
        class RuleBtoC(Rule): rule=([B], [C])
        self.assertFalse(g.have_rule(RuleBtoC))
        # Old rules
        class RuleNewSto0B0(Rule): rule = ([S], [0, B, 0])
        self.assertTrue(g.have_rule(RuleNewSto0B0))
        class RuleNewAto0A(Rule): rule = ([A], [0, A])
        self.assertTrue(g.have_rule(RuleNewAto0A))
        class RuleNewBto1B(Rule): rule = ([B], [1, B])
        self.assertTrue(g.have_rule(RuleNewBto1B))
        class RuleNewBtoAB(Rule): rule = ([B], [A, B])
        self.assertTrue(g.have_rule(RuleNewBtoAB))
        class RuleNewBtoEPS(Rule): rule = ([B], [EPS])
        self.assertTrue(g.have_rule(RuleNewBtoEPS))
        class RuleNewCto1A(Rule): rule = ([C], [1, A])
        self.assertTrue(g.have_rule(RuleNewCto1A))
        class RuleNewCto1(Rule): rule = ([C], [1])
        self.assertTrue(g.have_rule(RuleNewCto1))
        # New rules
        class RuleNewSto0A(Rule): rule = ([S], [0, A])
        self.assertTrue(g.have_rule(RuleNewSto0A))
        fromSto0A = g.get_rule(RuleNewSto0A)
        self.assertTrue(isclass(fromSto0A))
        self.assertTrue(issubclass(fromSto0A, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto0A.by_rules), 1)
        self.assertEqual(fromSto0A.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto0A.end_rule.rule, ([A], [0, A]))
        class RuleNewSto1B(Rule): rule = ([S], [1, B])
        self.assertTrue(g.have_rule(RuleNewSto1B))
        fromSto1B = g.get_rule(RuleNewSto1B)
        self.assertTrue(isclass(fromSto1B))
        self.assertTrue(issubclass(fromSto1B, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1B.by_rules), 2)
        self.assertEqual(fromSto1B.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1B.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromSto1B.end_rule.rule, ([B], [1, B]))
        class RuleNewStoAB(Rule): rule = ([S], [A, B])
        self.assertTrue(g.have_rule(RuleNewStoAB))
        fromStoAB = g.get_rule(RuleNewStoAB)
        self.assertTrue(isclass(fromStoAB))
        self.assertTrue(issubclass(fromStoAB, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromStoAB.by_rules), 2)
        self.assertEqual(fromStoAB.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromStoAB.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromStoAB.end_rule.rule, ([B], [A, B]))
        class RuleNewStoEPS(Rule): rule = ([S], [EPS])
        self.assertTrue(g.have_rule(RuleNewStoEPS))
        fromStoEPS = g.get_rule(RuleNewStoEPS)
        self.assertTrue(isclass(fromStoEPS))
        self.assertTrue(issubclass(fromStoEPS, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromStoEPS.by_rules), 2)
        self.assertEqual(fromStoEPS.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromStoEPS.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromStoEPS.end_rule.rule, ([B], [EPS]))
        class RuleNewSto1A(Rule): rule = ([S], [1, A])
        self.assertTrue(g.have_rule(RuleNewSto1A))
        fromSto1A = g.get_rule(RuleNewSto1A)
        self.assertTrue(isclass(fromSto1A))
        self.assertTrue(issubclass(fromSto1A, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1A.by_rules), 3)
        self.assertEqual(fromSto1A.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1A.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromSto1A.by_rules[2].rule, ([B], [C]))
        self.assertEqual(fromSto1A.end_rule.rule, ([C], [1, A]))
        class RuleNewSto1(Rule): rule = ([S], [1])
        self.assertTrue(g.have_rule(RuleNewSto1))
        fromSto1 = g.get_rule(RuleNewSto1)
        self.assertTrue(isclass(fromSto1))
        self.assertTrue(issubclass(fromSto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1.by_rules), 3)
        self.assertEqual(fromSto1.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1.by_rules[1].rule, ([A], [B]))
        self.assertEqual(fromSto1.by_rules[2].rule, ([B], [C]))
        self.assertEqual(fromSto1.end_rule.rule, ([C], [1]))
        class RuleNewAto1B(Rule): rule = ([A], [1, B])
        self.assertTrue(g.have_rule(RuleNewAto1B))
        fromAto1B = g.get_rule(RuleNewAto1B)
        self.assertTrue(isclass(fromAto1B))
        self.assertTrue(issubclass(fromAto1B, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto1B.by_rules), 1)
        self.assertEqual(fromAto1B.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAto1B.end_rule.rule, ([B], [1, B]))
        class RuleNewAtoAB(Rule): rule = ([A], [A, B])
        self.assertTrue(g.have_rule(RuleNewAtoAB))
        fromAtoAB = g.get_rule(RuleNewAtoAB)
        self.assertTrue(isclass(fromAtoAB))
        self.assertTrue(issubclass(fromAtoAB, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAtoAB.by_rules), 1)
        self.assertEqual(fromAtoAB.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAtoAB.end_rule.rule, ([B], [A, B]))
        class RuleNewAtoEPS(Rule): rule = ([A], [EPS])
        self.assertTrue(g.have_rule(RuleNewAtoEPS))
        fromAtoEPS = g.get_rule(RuleNewAtoEPS)
        self.assertTrue(isclass(fromAtoEPS))
        self.assertTrue(issubclass(fromAtoEPS, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAtoEPS.by_rules), 1)
        self.assertEqual(fromAtoEPS.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAtoEPS.end_rule.rule, ([B], [EPS]))
        class RuleNewAto1A(Rule): rule = ([A], [1, A])
        self.assertTrue(g.have_rule(RuleNewAto1A))
        fromAto1A = g.get_rule(RuleNewAto1A)
        self.assertTrue(isclass(fromAto1A))
        self.assertTrue(issubclass(fromAto1A, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto1A.by_rules), 2)
        self.assertEqual(fromAto1A.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAto1A.by_rules[1].rule, ([B], [C]))
        self.assertEqual(fromAto1A.end_rule.rule, ([C], [1, A]))
        class RuleNewAto1(Rule): rule = ([A], [1])
        self.assertTrue(g.have_rule(RuleNewAto1))
        fromAto1 = g.get_rule(RuleNewAto1)
        self.assertTrue(isclass(fromAto1))
        self.assertTrue(issubclass(fromAto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto1.by_rules), 2)
        self.assertEqual(fromAto1.by_rules[0].rule, ([A], [B]))
        self.assertEqual(fromAto1.by_rules[1].rule, ([B], [C]))
        self.assertEqual(fromAto1.end_rule.rule, ([C], [1]))
        class RuleNewBto1A(Rule): rule = ([B], [1, A])
        self.assertTrue(g.have_rule(RuleNewBto1A))
        fromBto1A = g.get_rule(RuleNewBto1A)
        self.assertTrue(isclass(fromBto1A))
        self.assertTrue(issubclass(fromBto1A, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto1A.by_rules), 1)
        self.assertEqual(fromBto1A.by_rules[0].rule, ([B], [C]))
        self.assertEqual(fromBto1A.end_rule.rule, ([C], [1, A]))
        class RuleNewBto1(Rule): rule = ([B], [1])
        self.assertTrue(g.have_rule(RuleNewBto1))
        fromBto1 = g.get_rule(RuleNewBto1)
        self.assertTrue(isclass(fromBto1))
        self.assertTrue(issubclass(fromBto1, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto1.by_rules), 1)
        self.assertEqual(fromBto1.by_rules[0].rule, ([B], [C]))
        self.assertEqual(fromBto1.end_rule.rule, ([C], [1]))


if __name__ == '__main__':
    main()
