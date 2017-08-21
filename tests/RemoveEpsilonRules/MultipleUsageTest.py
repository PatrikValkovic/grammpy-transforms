#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 15:55
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
class D(Nonterminal): pass
class Rules(Rule):
    rules = [
        ([S], [A, 0, A]),
        ([S], [0]),
        ([A], [B, C]),
        ([A], [2]),
        ([A], [C, C, C]), # multiple here
        ([B], [1, C]),
        ([B], [3, D]),
        ([B], [EPS]),
        ([C], [A, A, 3]),
        ([C], [EPS]),
        ([D], [A, A, B]),
        ([D], [A, A, 3])]

"""
S->A0A  S->0    A->BC   A->2    A->CCC  B->1C   B->3D   B->eps  C->AA3  C->eps  D->AAB  D->AA3
ToEpsilon: A, B, C, D
S->A0A  S->0    A->BC   A->2    A->CCC  B->1C   B->3D   B->eps  C->AA3  C->eps  D->AAB  D->AA3
                                                        ------          ------
                                                        
S->0A           A->C            A->CC   B->1    B->3            C->A3           D->AB   D->A3
S->A0           A->B                                                            D->AA 

                                                                C->3            D->B    D->3
                                                                                D->A
"""


class MultipleUsageTest(TestCase):
    def test_multipleUsage(self):
        g = Grammar(terminals=[0, 1, 2, 3],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        com = ContextFree.remove_rules_with_epsilon(g)
        self.assertEqual(len(com.rules()), 25)
        self.assertEqual(com.rules_count(), 25)
        class RuleNewSto0A(Rule): rule = ([S], [0, A])
        self.assertTrue(com.have_rule(RuleNewSto0A))
        fromSto0A = com.get_rule(RuleNewSto0A)
        self.assertTrue(isclass(fromSto0A))
        self.assertTrue(issubclass(fromSto0A, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromSto0A.from_rule.rule, ([S], [A, 0, A]))
        self.assertEqual(fromSto0A.replace_index, 0)
        class RuleNewStoA0(Rule): rule = ([S], [A, 0])
        self.assertTrue(com.have_rule(RuleNewStoA0))
        fromStoA0 = com.get_rule(RuleNewStoA0)
        self.assertTrue(isclass(fromStoA0))
        self.assertTrue(issubclass(fromStoA0, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoA0.from_rule.rule, ([S], [A, 0, A]))
        self.assertEqual(fromStoA0.replace_index, 2)
        class RuleNewAtoB(Rule): rule = ([A], [B])
        self.assertTrue(com.have_rule(RuleNewAtoB))
        fromAtoB = com.get_rule(RuleNewAtoB)
        self.assertTrue(isclass(fromAtoB))
        self.assertTrue(issubclass(fromAtoB, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromAtoB.from_rule.rule, ([A], [B, C]))
        self.assertEqual(fromAtoB.replace_index, 1)
        class RuleNewAtoC(Rule): rule = ([A], [C])
        self.assertTrue(com.have_rule(RuleNewAtoC))
        fromAtoC = com.get_rule(RuleNewAtoC)
        self.assertTrue(isclass(fromAtoC))
        self.assertTrue(issubclass(fromAtoC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromAtoC.from_rule.rule, ([A], [B, C]))
        self.assertEqual(fromAtoC.replace_index, 0)
        class RuleNewAtoCC(Rule): rule = ([A], [C, C])
        self.assertTrue(com.have_rule(RuleNewAtoCC))
        fromAtoCC = com.get_rule(RuleNewAtoCC)
        self.assertTrue(isclass(fromAtoCC))
        self.assertTrue(issubclass(fromAtoCC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromAtoCC.from_rule.rule, ([A], [C, C, C]))
        self.assertEqual(fromAtoCC.replace_index, 0)
        class RuleNewBto1(Rule): rule = ([B], [1])
        self.assertTrue(com.have_rule(RuleNewBto1))
        fromBto1 = com.get_rule(RuleNewBto1)
        self.assertTrue(isclass(fromBto1))
        self.assertTrue(issubclass(fromBto1, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromBto1.from_rule.rule, ([B], [1, C]))
        self.assertEqual(fromBto1.replace_index, 1)
        class RuleNewBto3(Rule): rule = ([B], [3])
        self.assertTrue(com.have_rule(RuleNewBto3))
        fromBto3 = com.get_rule(RuleNewBto3)
        self.assertTrue(isclass(fromBto3))
        self.assertTrue(issubclass(fromBto3, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromBto3.from_rule.rule, ([B], [3, D]))
        self.assertEqual(fromBto3.replace_index, 1)
        class RuleNewCtoA3(Rule): rule = ([C], [A, 3])
        self.assertTrue(com.have_rule(RuleNewCtoA3))
        fromCtoA3 = com.get_rule(RuleNewCtoA3)
        self.assertTrue(isclass(fromCtoA3))
        self.assertTrue(issubclass(fromCtoA3, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromCtoA3.from_rule.rule, ([C], [A, A, 3]))
        self.assertEqual(fromCtoA3.replace_index, 0)
        class RuleNewDtoAB(Rule): rule = ([D], [A, B])
        self.assertTrue(com.have_rule(RuleNewDtoAB))
        fromDtoAB = com.get_rule(RuleNewDtoAB)
        self.assertTrue(isclass(fromDtoAB))
        self.assertTrue(issubclass(fromDtoAB, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDtoAB.from_rule.rule, ([D], [A, A, B]))
        self.assertEqual(fromDtoAB.replace_index, 0)
        class RuleNewDtoAA(Rule): rule = ([D], [A, A])
        self.assertTrue(com.have_rule(RuleNewDtoAA))
        fromDtoAA = com.get_rule(RuleNewDtoAA)
        self.assertTrue(isclass(fromDtoAA))
        self.assertTrue(issubclass(fromDtoAA, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDtoAA.from_rule.rule, ([D], [A, A, B]))
        self.assertEqual(fromDtoAA.replace_index, 2)
        class RuleNewDtoA3(Rule): rule = ([D], [A, 3])
        self.assertTrue(com.have_rule(RuleNewDtoA3))
        fromDtoA3 = com.get_rule(RuleNewDtoA3)
        self.assertTrue(isclass(fromDtoA3))
        self.assertTrue(issubclass(fromDtoA3, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDtoA3.from_rule.rule, ([D], [A, A, 3]))
        self.assertEqual(fromDtoA3.replace_index, 0)
        class RuleNewCto3(Rule): rule = ([C], [3])
        self.assertTrue(com.have_rule(RuleNewCto3))
        fromCto3 = com.get_rule(RuleNewCto3)
        self.assertTrue(isclass(fromCto3))
        self.assertTrue(issubclass(fromCto3, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromCto3.from_rule.rule, ([C], [A, 3]))
        self.assertEqual(fromCto3.replace_index, 0)
        class RuleNewDtoA(Rule): rule = ([D], [A])
        self.assertTrue(com.have_rule(RuleNewDtoA))
        fromDtoA = com.get_rule(RuleNewDtoA)
        self.assertTrue(isclass(fromDtoA))
        self.assertTrue(issubclass(fromDtoA, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDtoA.from_rule.rule, ([D], [A, B]))
        self.assertEqual(fromDtoA.replace_index, 1)
        class RuleNewDtoB(Rule): rule = ([D], [B])
        self.assertTrue(com.have_rule(RuleNewDtoB))
        fromDtoB = com.get_rule(RuleNewDtoB)
        self.assertTrue(isclass(fromDtoB))
        self.assertTrue(issubclass(fromDtoB, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDtoB.from_rule.rule, ([D], [A, B]))
        self.assertEqual(fromDtoB.replace_index, 0)
        class RuleNewDto3(Rule): rule = ([D], [3])
        self.assertTrue(com.have_rule(RuleNewDto3))
        fromDto3 = com.get_rule(RuleNewDto3)
        self.assertTrue(isclass(fromDto3))
        self.assertTrue(issubclass(fromDto3, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDto3.from_rule.rule, ([D], [A, 3]))
        self.assertEqual(fromDto3.replace_index, 0)
        class BtoEps(Rule): rule=([B], [EPS])
        class CtoEps(Rule): rule=([B], [EPS])
        self.assertFalse(com.have_rule(BtoEps))
        self.assertFalse(com.have_rule(CtoEps))

    def test_multipleUsageShouldNotChange(self):
        g = Grammar(terminals=[0, 1, 2, 3],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_rules_with_epsilon(g)
        self.assertEqual(len(g.rules()), 12)
        self.assertEqual(g.rules_count(), 12)
        class RuleNewAto0A(Rule): rule = ([A], [0, A])
        class RuleNewAtoA0(Rule): rule = ([A], [A, 0])
        class RuleNewAtoB(Rule): rule = ([A], [B])
        class RuleNewAtoC(Rule): rule = ([A], [C])
        class RuleNewAtoCC(Rule): rule = ([A], [C, C])
        class RuleNewAto1(Rule): rule = ([A], [1])
        class RuleNewBto3(Rule): rule = ([B], [3])
        class RuleNewCtoA3(Rule): rule = ([C], [A, 3])
        class RuleNewDtoAB(Rule): rule = ([D], [A, B])
        class RuleNewDtoAA(Rule): rule = ([D], [A, A])
        class RuleNewDtoA3(Rule): rule = ([D], [A, 3])
        class RuleNewCto3(Rule): rule = ([C], [3])
        class RuleNewDtoA(Rule): rule = ([D], [A])
        class RuleNewDtoB(Rule): rule = ([D], [B])
        class RuleNewDto3(Rule): rule = ([D], [3])
        self.assertFalse(g.have_rule(RuleNewAto0A))
        self.assertFalse(g.have_rule(RuleNewAtoA0))
        self.assertFalse(g.have_rule(RuleNewAtoB))
        self.assertFalse(g.have_rule(RuleNewAtoC))
        self.assertFalse(g.have_rule(RuleNewAtoCC))
        self.assertFalse(g.have_rule(RuleNewAto1))
        self.assertFalse(g.have_rule(RuleNewBto3))
        self.assertFalse(g.have_rule(RuleNewCtoA3))
        self.assertFalse(g.have_rule(RuleNewDtoAB))
        self.assertFalse(g.have_rule(RuleNewDtoAA))
        self.assertFalse(g.have_rule(RuleNewDtoA3))
        self.assertFalse(g.have_rule(RuleNewCto3))
        self.assertFalse(g.have_rule(RuleNewDtoA))
        self.assertFalse(g.have_rule(RuleNewDtoB))
        self.assertFalse(g.have_rule(RuleNewDto3))
        class BtoEps(Rule): rule=([B], [EPS])
        class CtoEps(Rule): rule=([B], [EPS])
        self.assertTrue(g.have_rule(BtoEps))
        self.assertTrue(g.have_rule(CtoEps))

    def test_multipleUsageShouldChange(self):
        g = Grammar(terminals=[0, 1, 2, 3],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        ContextFree.remove_rules_with_epsilon(g, transform_grammar=True)
        self.assertEqual(len(g.rules()), 25)
        self.assertEqual(g.rules_count(), 25)
        class RuleNewSto0A(Rule): rule = ([S], [0, A])
        self.assertTrue(g.have_rule(RuleNewSto0A))
        fromSto0A = g.get_rule(RuleNewSto0A)
        self.assertTrue(isclass(fromSto0A))
        self.assertTrue(issubclass(fromSto0A, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromSto0A.from_rule.rule, ([S], [A, 0, A]))
        self.assertEqual(fromSto0A.replace_index, 0)
        class RuleNewStoA0(Rule): rule = ([S], [A, 0])
        self.assertTrue(g.have_rule(RuleNewStoA0))
        fromStoA0 = g.get_rule(RuleNewStoA0)
        self.assertTrue(isclass(fromStoA0))
        self.assertTrue(issubclass(fromStoA0, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromStoA0.from_rule.rule, ([S], [A, 0, A]))
        self.assertEqual(fromStoA0.replace_index, 2)
        class RuleNewAtoB(Rule): rule = ([A], [B])
        self.assertTrue(g.have_rule(RuleNewAtoB))
        fromAtoB = g.get_rule(RuleNewAtoB)
        self.assertTrue(isclass(fromAtoB))
        self.assertTrue(issubclass(fromAtoB, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromAtoB.from_rule.rule, ([A], [B, C]))
        self.assertEqual(fromAtoB.replace_index, 1)
        class RuleNewAtoC(Rule): rule = ([A], [C])
        self.assertTrue(g.have_rule(RuleNewAtoC))
        fromAtoC = g.get_rule(RuleNewAtoC)
        self.assertTrue(isclass(fromAtoC))
        self.assertTrue(issubclass(fromAtoC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromAtoC.from_rule.rule, ([A], [B, C]))
        self.assertEqual(fromAtoC.replace_index, 0)
        class RuleNewAtoCC(Rule): rule = ([A], [C, C])
        self.assertTrue(g.have_rule(RuleNewAtoCC))
        fromAtoCC = g.get_rule(RuleNewAtoCC)
        self.assertTrue(isclass(fromAtoCC))
        self.assertTrue(issubclass(fromAtoCC, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromAtoCC.from_rule.rule, ([A], [C, C, C]))
        self.assertEqual(fromAtoCC.replace_index, 0)
        class RuleNewBto1(Rule): rule = ([B], [1])
        self.assertTrue(g.have_rule(RuleNewBto1))
        fromBto1 = g.get_rule(RuleNewBto1)
        self.assertTrue(isclass(fromBto1))
        self.assertTrue(issubclass(fromBto1, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromBto1.from_rule.rule, ([B], [1, C]))
        self.assertEqual(fromBto1.replace_index, 1)
        class RuleNewBto3(Rule): rule = ([B], [3])
        self.assertTrue(g.have_rule(RuleNewBto3))
        fromBto3 = g.get_rule(RuleNewBto3)
        self.assertTrue(isclass(fromBto3))
        self.assertTrue(issubclass(fromBto3, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromBto3.from_rule.rule, ([B], [3, D]))
        self.assertEqual(fromBto3.replace_index, 1)
        class RuleNewCtoA3(Rule): rule = ([C], [A, 3])
        self.assertTrue(g.have_rule(RuleNewCtoA3))
        fromCtoA3 = g.get_rule(RuleNewCtoA3)
        self.assertTrue(isclass(fromCtoA3))
        self.assertTrue(issubclass(fromCtoA3, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromCtoA3.from_rule.rule, ([C], [A, A, 3]))
        self.assertEqual(fromCtoA3.replace_index, 0)
        class RuleNewDtoAB(Rule): rule = ([D], [A, B])
        self.assertTrue(g.have_rule(RuleNewDtoAB))
        fromDtoAB = g.get_rule(RuleNewDtoAB)
        self.assertTrue(isclass(fromDtoAB))
        self.assertTrue(issubclass(fromDtoAB, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDtoAB.from_rule.rule, ([D], [A, A, B]))
        self.assertEqual(fromDtoAB.replace_index, 0)
        class RuleNewDtoAA(Rule): rule = ([D], [A, A])
        self.assertTrue(g.have_rule(RuleNewDtoAA))
        fromDtoAA = g.get_rule(RuleNewDtoAA)
        self.assertTrue(isclass(fromDtoAA))
        self.assertTrue(issubclass(fromDtoAA, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDtoAA.from_rule.rule, ([D], [A, A, B]))
        self.assertEqual(fromDtoAA.replace_index, 2)
        class RuleNewDtoA3(Rule): rule = ([D], [A, 3])
        self.assertTrue(g.have_rule(RuleNewDtoA3))
        fromDtoA3 = g.get_rule(RuleNewDtoA3)
        self.assertTrue(isclass(fromDtoA3))
        self.assertTrue(issubclass(fromDtoA3, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDtoA3.from_rule.rule, ([D], [A, A, 3]))
        self.assertEqual(fromDtoA3.replace_index, 0)
        class RuleNewCto3(Rule): rule = ([C], [3])
        self.assertTrue(g.have_rule(RuleNewCto3))
        fromCto3 = g.get_rule(RuleNewCto3)
        self.assertTrue(isclass(fromCto3))
        self.assertTrue(issubclass(fromCto3, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromCto3.from_rule.rule, ([C], [A, 3]))
        self.assertEqual(fromCto3.replace_index, 0)
        class RuleNewDtoA(Rule): rule = ([D], [A])
        self.assertTrue(g.have_rule(RuleNewDtoA))
        fromDtoA = g.get_rule(RuleNewDtoA)
        self.assertTrue(isclass(fromDtoA))
        self.assertTrue(issubclass(fromDtoA, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDtoA.from_rule.rule, ([D], [A, B]))
        self.assertEqual(fromDtoA.replace_index, 1)
        class RuleNewDtoB(Rule): rule = ([D], [B])
        self.assertTrue(g.have_rule(RuleNewDtoB))
        fromDtoB = g.get_rule(RuleNewDtoB)
        self.assertTrue(isclass(fromDtoB))
        self.assertTrue(issubclass(fromDtoB, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDtoB.from_rule.rule, ([D], [A, B]))
        self.assertEqual(fromDtoB.replace_index, 0)
        class RuleNewDto3(Rule): rule = ([D], [3])
        self.assertTrue(g.have_rule(RuleNewDto3))
        fromDto3 = g.get_rule(RuleNewDto3)
        self.assertTrue(isclass(fromDto3))
        self.assertTrue(issubclass(fromDto3, ContextFree.EpsilonRemovedRule))
        self.assertEqual(fromDto3.from_rule.rule, ([D], [A, 3]))
        self.assertEqual(fromDto3.replace_index, 0)
        class BtoEps(Rule): rule=([B], [EPS])
        class CtoEps(Rule): rule=([B], [EPS])
        self.assertFalse(g.have_rule(BtoEps))
        self.assertFalse(g.have_rule(CtoEps))




if __name__ == '__main__':
    main()
