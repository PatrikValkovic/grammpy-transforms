#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 20:51
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

S->A  S->B  A->C  A->0A  A->1S  B->D  B->2B  B->3S  C->1C  C->0  D->3D  D->2
----  ----  ----                ----                         

S->A->0A
S->A->1S
S->A->C->1C
S->A->C->0
S->B->2B
S->B->3S
S->B->D->3D
S->B->D->2
A->C->1C
A->C->0
B->D->3D
B->D->2
"""


class SimpleTest(TestCase):
    def test_simpleTest(self):
        g = Grammar(terminals=[0,1,2,3],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        com = ContextFree.remove_unit_rules(g)
        # Removed
        class RuleStoA(Rule): rule=([S], [A])
        self.assertFalse(com.have_rule(RuleStoA))
        class RuleStoB(Rule): rule=([S], [B])
        self.assertFalse(com.have_rule(RuleStoB))
        class RuleAtoC(Rule): rule=([A], [C])
        self.assertFalse(com.have_rule(RuleAtoC))
        class RuleBtoD(Rule): rule=([B], [D])
        self.assertFalse(com.have_rule(RuleBtoD))
        # Old rules
        class RuleNewAto0A(Rule): rule = ([A], [0, A])
        self.assertTrue(com.have_rule(RuleNewAto0A))
        class RuleNewAto1S(Rule): rule = ([A], [1, S])
        self.assertTrue(com.have_rule(RuleNewAto1S))
        class RuleNewBto2B(Rule): rule = ([B], [2, B])
        self.assertTrue(com.have_rule(RuleNewBto2B))
        class RuleNewBto3S(Rule): rule = ([B], [3, S])
        self.assertTrue(com.have_rule(RuleNewBto3S))
        class RuleNewCto1C(Rule): rule = ([C], [1, C])
        self.assertTrue(com.have_rule(RuleNewCto1C))
        class RuleNewCto0(Rule): rule = ([C], [0])
        self.assertTrue(com.have_rule(RuleNewCto0))
        class RuleNewDto3D(Rule): rule = ([D], [3, D])
        self.assertTrue(com.have_rule(RuleNewDto3D))
        class RuleNewDto2(Rule): rule = ([D], [2])
        self.assertTrue(com.have_rule(RuleNewDto2))
        # New rules
        class RuleNewSto0A(Rule): rule = ([S], [0, A])
        self.assertTrue(com.have_rule(RuleNewSto0A))
        fromSto0A = com.get_rule(RuleNewSto0A)
        self.assertTrue(isclass(fromSto0A))
        self.assertTrue(issubclass(fromSto0A, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto0A.by_rules), 1)
        self.assertEqual(fromSto0A.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto0A.end_rule.rule, ([A], [0, A]))
        class RuleNewSto1S(Rule): rule = ([S], [1, S])
        self.assertTrue(com.have_rule(RuleNewSto1S))
        fromSto1S = com.get_rule(RuleNewSto1S)
        self.assertTrue(isclass(fromSto1S))
        self.assertTrue(issubclass(fromSto1S, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1S.by_rules), 1)
        self.assertEqual(fromSto1S.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1S.end_rule.rule, ([A], [1, S]))
        class RuleNewSto1C(Rule): rule = ([S], [1, C])
        self.assertTrue(com.have_rule(RuleNewSto1C))
        fromSto1C = com.get_rule(RuleNewSto1C)
        self.assertTrue(isclass(fromSto1C))
        self.assertTrue(issubclass(fromSto1C, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1C.by_rules), 2)
        self.assertEqual(fromSto1C.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1C.by_rules[1].rule, ([A], [C]))
        self.assertEqual(fromSto1C.end_rule.rule, ([C], [1, C]))
        class RuleNewSto0(Rule): rule = ([S], [0])
        self.assertTrue(com.have_rule(RuleNewSto0))
        fromSto0 = com.get_rule(RuleNewSto0)
        self.assertTrue(isclass(fromSto0))
        self.assertTrue(issubclass(fromSto0, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto0.by_rules), 2)
        self.assertEqual(fromSto0.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto0.by_rules[1].rule, ([A], [C]))
        self.assertEqual(fromSto0.end_rule.rule, ([C], [0]))
        class RuleNewSto2B(Rule): rule = ([S], [2, B])
        self.assertTrue(com.have_rule(RuleNewSto2B))
        fromSto2B = com.get_rule(RuleNewSto2B)
        self.assertTrue(isclass(fromSto2B))
        self.assertTrue(issubclass(fromSto2B, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto2B.by_rules), 1)
        self.assertEqual(fromSto2B.by_rules[0].rule, ([S], [B]))
        self.assertEqual(fromSto2B.end_rule.rule, ([B], [2, B]))
        class RuleNewSto3S(Rule): rule = ([S], [3, S])
        self.assertTrue(com.have_rule(RuleNewSto3S))
        fromSto3S = com.get_rule(RuleNewSto3S)
        self.assertTrue(isclass(fromSto3S))
        self.assertTrue(issubclass(fromSto3S, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto3S.by_rules), 1)
        self.assertEqual(fromSto3S.by_rules[0].rule, ([S], [B]))
        self.assertEqual(fromSto3S.end_rule.rule, ([B], [3, S]))
        class RuleNewSto3D(Rule): rule = ([S], [3, D])
        self.assertTrue(com.have_rule(RuleNewSto3D))
        fromSto3D = com.get_rule(RuleNewSto3D)
        self.assertTrue(isclass(fromSto3D))
        self.assertTrue(issubclass(fromSto3D, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto3D.by_rules), 2)
        self.assertEqual(fromSto3D.by_rules[0].rule, ([S], [B]))
        self.assertEqual(fromSto3D.by_rules[1].rule, ([B], [D]))
        self.assertEqual(fromSto3D.end_rule.rule, ([D], [3, D]))
        class RuleNewSto2(Rule): rule = ([S], [2])
        self.assertTrue(com.have_rule(RuleNewSto2))
        fromSto2 = com.get_rule(RuleNewSto2)
        self.assertTrue(isclass(fromSto2))
        self.assertTrue(issubclass(fromSto2, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto2.by_rules), 2)
        self.assertEqual(fromSto2.by_rules[0].rule, ([S], [B]))
        self.assertEqual(fromSto2.by_rules[1].rule, ([B], [D]))
        self.assertEqual(fromSto2.end_rule.rule, ([D], [2]))
        class RuleNewAto1C(Rule): rule = ([A], [1, C])
        self.assertTrue(com.have_rule(RuleNewAto1C))
        fromAto1C = com.get_rule(RuleNewAto1C)
        self.assertTrue(isclass(fromAto1C))
        self.assertTrue(issubclass(fromAto1C, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto1C.by_rules), 1)
        self.assertEqual(fromAto1C.by_rules[0].rule, ([A], [C]))
        self.assertEqual(fromAto1C.end_rule.rule, ([C], [1, C]))
        class RuleNewAto0(Rule): rule = ([A], [0])
        self.assertTrue(com.have_rule(RuleNewAto0))
        fromAto0 = com.get_rule(RuleNewAto0)
        self.assertTrue(isclass(fromAto0))
        self.assertTrue(issubclass(fromAto0, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto0.by_rules), 1)
        self.assertEqual(fromAto0.by_rules[0].rule, ([A], [C]))
        self.assertEqual(fromAto0.end_rule.rule, ([C], [0]))
        class RuleNewBto3D(Rule): rule = ([B], [3, D])
        self.assertTrue(com.have_rule(RuleNewBto3D))
        fromBto3D = com.get_rule(RuleNewBto3D)
        self.assertTrue(isclass(fromBto3D))
        self.assertTrue(issubclass(fromBto3D, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto3D.by_rules), 1)
        self.assertEqual(fromBto3D.by_rules[0].rule, ([B], [D]))
        self.assertEqual(fromBto3D.end_rule.rule, ([D], [3, D]))
        class RuleNewBto2(Rule): rule = ([B], [2])
        self.assertTrue(com.have_rule(RuleNewBto2))
        fromBto2 = com.get_rule(RuleNewBto2)
        self.assertTrue(isclass(fromBto2))
        self.assertTrue(issubclass(fromBto2, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto2.by_rules), 1)
        self.assertEqual(fromBto2.by_rules[0].rule, ([B], [D]))
        self.assertEqual(fromBto2.end_rule.rule, ([D], [2]))

    def test_simpleTestShouldNotChange(self):
        g = Grammar(terminals=[0,1,2,3],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_unit_rules(g)
        # Removed
        class RuleStoA(Rule): rule = ([S], [A])
        self.assertTrue(g.have_rule(RuleStoA))
        class RuleStoB(Rule): rule = ([S], [B])
        self.assertTrue(g.have_rule(RuleStoB))
        class RuleAtoC(Rule): rule = ([A], [C])
        self.assertTrue(g.have_rule(RuleAtoC))
        class RuleBtoD(Rule): rule = ([B], [D])
        self.assertTrue(g.have_rule(RuleBtoD))
        # Old rules
        class RuleNewAto0A(Rule): rule = ([A], [0, A])
        self.assertTrue(g.have_rule(RuleNewAto0A))
        class RuleNewAto1S(Rule): rule = ([A], [1, S])
        self.assertTrue(g.have_rule(RuleNewAto1S))
        class RuleNewBto2B(Rule): rule = ([B], [2, B])
        self.assertTrue(g.have_rule(RuleNewBto2B))
        class RuleNewBto3S(Rule): rule = ([B], [3, S])
        self.assertTrue(g.have_rule(RuleNewBto3S))
        class RuleNewCto1C(Rule): rule = ([C], [1, C])
        self.assertTrue(g.have_rule(RuleNewCto1C))
        class RuleNewCto0(Rule): rule = ([C], [0])
        self.assertTrue(g.have_rule(RuleNewCto0))
        class RuleNewDto3D(Rule): rule = ([D], [3, D])
        self.assertTrue(g.have_rule(RuleNewDto3D))
        class RuleNewDto2(Rule): rule = ([D], [2])
        self.assertTrue(g.have_rule(RuleNewDto2))
        # New rules
        class RuleNewSto0A(Rule): rule = ([S], [0, A])
        self.assertFalse(g.have_rule(RuleNewSto0A))
        class RuleNewSto1S(Rule): rule = ([S], [1, S])
        self.assertFalse(g.have_rule(RuleNewSto1S))
        class RuleNewSto1C(Rule): rule = ([S], [1, C])
        self.assertFalse(g.have_rule(RuleNewSto1C))
        class RuleNewSto0(Rule): rule = ([S], [0])
        self.assertFalse(g.have_rule(RuleNewSto0))
        class RuleNewSto2B(Rule): rule = ([S], [2, B])
        self.assertFalse(g.have_rule(RuleNewSto2B))
        class RuleNewSto3S(Rule): rule = ([S], [3, S])
        self.assertFalse(g.have_rule(RuleNewSto3S))
        class RuleNewSto3D(Rule): rule = ([S], [3, D])
        self.assertFalse(g.have_rule(RuleNewSto3D))
        class RuleNewSto2(Rule): rule = ([S], [2])
        self.assertFalse(g.have_rule(RuleNewSto2))
        class RuleNewAto1C(Rule): rule = ([A], [1, C])
        self.assertFalse(g.have_rule(RuleNewAto1C))
        class RuleNewAto0(Rule): rule = ([A], [0])
        self.assertFalse(g.have_rule(RuleNewAto0))
        class RuleNewBto3D(Rule): rule = ([B], [3, D])
        self.assertFalse(g.have_rule(RuleNewBto3D))
        class RuleNewBto2(Rule): rule = ([B], [2])
        self.assertFalse(g.have_rule(RuleNewBto2))

    def test_simpleTestShouldChange(self):
        g = Grammar(terminals=[0,1,2,3],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_unit_rules(g, transform_grammar=True)
        # Removed
        class RuleStoA(Rule): rule=([S], [A])
        self.assertFalse(g.have_rule(RuleStoA))
        class RuleStoB(Rule): rule=([S], [B])
        self.assertFalse(g.have_rule(RuleStoB))
        class RuleAtoC(Rule): rule=([A], [C])
        self.assertFalse(g.have_rule(RuleAtoC))
        class RuleBtoD(Rule): rule=([B], [D])
        self.assertFalse(g.have_rule(RuleBtoD))
        # Old rules
        class RuleNewAto0A(Rule): rule = ([A], [0, A])
        self.assertTrue(g.have_rule(RuleNewAto0A))
        class RuleNewAto1S(Rule): rule = ([A], [1, S])
        self.assertTrue(g.have_rule(RuleNewAto1S))
        class RuleNewBto2B(Rule): rule = ([B], [2, B])
        self.assertTrue(g.have_rule(RuleNewBto2B))
        class RuleNewBto3S(Rule): rule = ([B], [3, S])
        self.assertTrue(g.have_rule(RuleNewBto3S))
        class RuleNewCto1C(Rule): rule = ([C], [1, C])
        self.assertTrue(g.have_rule(RuleNewCto1C))
        class RuleNewCto0(Rule): rule = ([C], [0])
        self.assertTrue(g.have_rule(RuleNewCto0))
        class RuleNewDto3D(Rule): rule = ([D], [3, D])
        self.assertTrue(g.have_rule(RuleNewDto3D))
        class RuleNewDto2(Rule): rule = ([D], [2])
        self.assertTrue(g.have_rule(RuleNewDto2))
        # New rules
        class RuleNewSto0A(Rule): rule = ([S], [0, A])
        self.assertTrue(g.have_rule(RuleNewSto0A))
        fromSto0A = g.get_rule(RuleNewSto0A)
        self.assertTrue(isclass(fromSto0A))
        self.assertTrue(issubclass(fromSto0A, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto0A.by_rules), 1)
        self.assertEqual(fromSto0A.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto0A.end_rule.rule, ([A], [0, A]))
        class RuleNewSto1S(Rule): rule = ([S], [1, S])
        self.assertTrue(g.have_rule(RuleNewSto1S))
        fromSto1S = g.get_rule(RuleNewSto1S)
        self.assertTrue(isclass(fromSto1S))
        self.assertTrue(issubclass(fromSto1S, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1S.by_rules), 1)
        self.assertEqual(fromSto1S.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1S.end_rule.rule, ([A], [1, S]))
        class RuleNewSto1C(Rule): rule = ([S], [1, C])
        self.assertTrue(g.have_rule(RuleNewSto1C))
        fromSto1C = g.get_rule(RuleNewSto1C)
        self.assertTrue(isclass(fromSto1C))
        self.assertTrue(issubclass(fromSto1C, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto1C.by_rules), 2)
        self.assertEqual(fromSto1C.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto1C.by_rules[1].rule, ([A], [C]))
        self.assertEqual(fromSto1C.end_rule.rule, ([C], [1, C]))
        class RuleNewSto0(Rule): rule = ([S], [0])
        self.assertTrue(g.have_rule(RuleNewSto0))
        fromSto0 = g.get_rule(RuleNewSto0)
        self.assertTrue(isclass(fromSto0))
        self.assertTrue(issubclass(fromSto0, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto0.by_rules), 2)
        self.assertEqual(fromSto0.by_rules[0].rule, ([S], [A]))
        self.assertEqual(fromSto0.by_rules[1].rule, ([A], [C]))
        self.assertEqual(fromSto0.end_rule.rule, ([C], [0]))
        class RuleNewSto2B(Rule): rule = ([S], [2, B])
        self.assertTrue(g.have_rule(RuleNewSto2B))
        fromSto2B = g.get_rule(RuleNewSto2B)
        self.assertTrue(isclass(fromSto2B))
        self.assertTrue(issubclass(fromSto2B, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto2B.by_rules), 1)
        self.assertEqual(fromSto2B.by_rules[0].rule, ([S], [B]))
        self.assertEqual(fromSto2B.end_rule.rule, ([B], [2, B]))
        class RuleNewSto3S(Rule): rule = ([S], [3, S])
        self.assertTrue(g.have_rule(RuleNewSto3S))
        fromSto3S = g.get_rule(RuleNewSto3S)
        self.assertTrue(isclass(fromSto3S))
        self.assertTrue(issubclass(fromSto3S, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto3S.by_rules), 1)
        self.assertEqual(fromSto3S.by_rules[0].rule, ([S], [B]))
        self.assertEqual(fromSto3S.end_rule.rule, ([B], [3, S]))
        class RuleNewSto3D(Rule): rule = ([S], [3, D])
        self.assertTrue(g.have_rule(RuleNewSto3D))
        fromSto3D = g.get_rule(RuleNewSto3D)
        self.assertTrue(isclass(fromSto3D))
        self.assertTrue(issubclass(fromSto3D, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto3D.by_rules), 2)
        self.assertEqual(fromSto3D.by_rules[0].rule, ([S], [B]))
        self.assertEqual(fromSto3D.by_rules[1].rule, ([B], [D]))
        self.assertEqual(fromSto3D.end_rule.rule, ([D], [3, D]))
        class RuleNewSto2(Rule): rule = ([S], [2])
        self.assertTrue(g.have_rule(RuleNewSto2))
        fromSto2 = g.get_rule(RuleNewSto2)
        self.assertTrue(isclass(fromSto2))
        self.assertTrue(issubclass(fromSto2, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromSto2.by_rules), 2)
        self.assertEqual(fromSto2.by_rules[0].rule, ([S], [B]))
        self.assertEqual(fromSto2.by_rules[1].rule, ([B], [D]))
        self.assertEqual(fromSto2.end_rule.rule, ([D], [2]))
        class RuleNewAto1C(Rule): rule = ([A], [1, C])
        self.assertTrue(g.have_rule(RuleNewAto1C))
        fromAto1C = g.get_rule(RuleNewAto1C)
        self.assertTrue(isclass(fromAto1C))
        self.assertTrue(issubclass(fromAto1C, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto1C.by_rules), 1)
        self.assertEqual(fromAto1C.by_rules[0].rule, ([A], [C]))
        self.assertEqual(fromAto1C.end_rule.rule, ([C], [1, C]))
        class RuleNewAto0(Rule): rule = ([A], [0])
        self.assertTrue(g.have_rule(RuleNewAto0))
        fromAto0 = g.get_rule(RuleNewAto0)
        self.assertTrue(isclass(fromAto0))
        self.assertTrue(issubclass(fromAto0, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromAto0.by_rules), 1)
        self.assertEqual(fromAto0.by_rules[0].rule, ([A], [C]))
        self.assertEqual(fromAto0.end_rule.rule, ([C], [0]))
        class RuleNewBto3D(Rule): rule = ([B], [3, D])
        self.assertTrue(g.have_rule(RuleNewBto3D))
        fromBto3D = g.get_rule(RuleNewBto3D)
        self.assertTrue(isclass(fromBto3D))
        self.assertTrue(issubclass(fromBto3D, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto3D.by_rules), 1)
        self.assertEqual(fromBto3D.by_rules[0].rule, ([B], [D]))
        self.assertEqual(fromBto3D.end_rule.rule, ([D], [3, D]))
        class RuleNewBto2(Rule): rule = ([B], [2])
        self.assertTrue(g.have_rule(RuleNewBto2))
        fromBto2 = g.get_rule(RuleNewBto2)
        self.assertTrue(isclass(fromBto2))
        self.assertTrue(issubclass(fromBto2, ContextFree.ReducedUnitRule))
        self.assertEqual(len(fromBto2.by_rules), 1)
        self.assertEqual(fromBto2.by_rules[0].rule, ([B], [D]))
        self.assertEqual(fromBto2.end_rule.rule, ([D], [2]))

if __name__ == '__main__':
    main()
