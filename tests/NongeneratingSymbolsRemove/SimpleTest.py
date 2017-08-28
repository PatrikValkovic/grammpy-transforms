#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.06.2017 16:39
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import ContextFree


class A(Nonterminal):
    pass


class B(Nonterminal):
    pass


class C(Nonterminal):
    pass


class RuleAto0B(Rule):
    fromSymbol = A
    right = [0, B]


class RuleBto1(Rule):
    fromSymbol = B
    toSymbol = 1


class SimpleTest(TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.g = Grammar()

    def setUp(self):
        self.g = Grammar(terminals=[0, 1],
                    nonterminals=[A, B, C],
                    rules=[RuleAto0B, RuleBto1])

    def test_simpleTest(self):
        changed = ContextFree.remove_nongenerating_nonterminals(self.g)
        self.assertTrue(changed.have_term([0, 1]))
        self.assertTrue(changed.have_nonterm([A, B]))
        self.assertFalse(changed.have_nonterm(C))

    def test_simpleTestWithoutChange(self):
        ContextFree.remove_nongenerating_nonterminals(self.g)
        self.assertTrue(self.g.have_term([0, 1]))
        self.assertTrue(self.g.have_nonterm([A, B, C]))

    def test_simpleTestWithChange(self):
        changed = ContextFree.remove_nongenerating_nonterminals(self.g, transform_grammar=True)
        self.assertEqual(id(changed), id(self.g))
        self.assertTrue(self.g.have_term([0, 1]))
        self.assertTrue(self.g.have_nonterm([A, B]))
        self.assertFalse(self.g.have_nonterm(C))


if __name__ == '__main__':
    main()
