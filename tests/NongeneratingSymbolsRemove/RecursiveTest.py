#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.06.2017 16:39
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import *


class A(Nonterminal):
    pass


class B(Nonterminal):
    pass


class C(Nonterminal):
    pass


class D(Nonterminal):
    pass


class E(Nonterminal):
    pass


class RuleAto0B(Rule):
    rule = ([A], [0, B])


class RuleBto1(Rule):
    fromSymbol = B
    toSymbol = 1


class RuleCto1D(Rule):
    rule = ([C], [1, D])


class RuleDto0E(Rule):
    rule = ([D], [0, E])


class RuleEto0C(Rule):
    rule = ([E], [0, C])


class RecursiveTest(TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.g = Grammar()

    def setUp(self):
        self.g = Grammar(terminals=[0, 1],
                         nonterminals=[A, B, C, D, E],
                         rules=[RuleAto0B, RuleBto1,
                                RuleCto1D, RuleDto0E,
                                RuleEto0C])

    def test_recursiveTest(self):
        changed = ContextFree.remove_nongenerating_nonterminals(self.g)
        self.assertTrue(changed.have_term([0, 1]))
        self.assertTrue(changed.have_nonterm([A, B]))
        self.assertFalse(changed.have_nonterm(C))
        self.assertFalse(changed.have_nonterm(D))
        self.assertFalse(changed.have_nonterm(E))

    def test_recursiveTestWithoutChange(self):
        ContextFree.remove_nongenerating_nonterminals(self.g)
        self.assertTrue(self.g.have_term([0, 1]))
        self.assertTrue(self.g.have_nonterm([A, B, C, D, E]))

    def test_recursiveTestWithChange(self):
        changed = ContextFree.remove_nongenerating_nonterminals(self.g, transform_grammar=True)
        self.assertEqual(id(changed), id(self.g))
        self.assertTrue(self.g.have_term([0, 1]))
        self.assertTrue(self.g.have_nonterm([A, B]))
        self.assertFalse(self.g.have_nonterm(C))
        self.assertFalse(self.g.have_nonterm(D))
        self.assertFalse(self.g.have_nonterm(E))

if __name__ == '__main__':
    main()
