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
    def test_simpleTest(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[A, B, C],
                    rules=[RuleAto0B, RuleBto1])
        changed = ContextFree.remove_nongenerastingSymbols(g)
        self.assertTrue(changed.have_term([0, 1]))
        self.assertTrue(changed.have_nonterm([A, B]))
        self.assertFalse(changed.have_nonterm(C))


if __name__ == '__main__':
    main()
