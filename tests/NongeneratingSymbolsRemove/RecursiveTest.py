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
                         nonterminals=[A, B],
                         rules=[RuleAto0B, RuleBto1, RuleCto1D, RuleDto0E, RuleEto0C])


if __name__ == '__main__':
    main()
