#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 16.08.2017 18:18
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import main, TestCase
from grammpy import *
from grammpy_transforms import ContextFree


class A(Nonterminal):
    pass
class B(Nonterminal):
    pass
class C(Nonterminal):
    pass
class RuleAto0B(Rule):
    rule = ([A], [0, B])
class RuleBto01(Rule):
    rule = ([B], [0, 1])
class RuleAto1C(Rule):
    rule = ([A], [1, C])
class RuleCto0C(Rule):
    rule = ([C], [0, C])


class PartCompleteTest(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.g = Grammar()

    def setUp(self):
        self.g = Grammar(terminals=[0, 1, 2],
                         nonterminals=[A, B, C],
                         rules=[RuleAto0B, RuleBto01,
                                RuleAto1C, RuleCto0C])

    def test_partlyIncompleteTest(self):
        changed = ContextFree.remove_nongenerating_nonterminals(self.g)
        self.assertTrue(changed.have_term([0, 1]))
        self.assertTrue(changed.have_nonterm([A, B]))
        self.assertFalse(changed.have_nonterm(C))

    def test_partlyIncompleteTestWithoutChange(self):
        ContextFree.remove_nongenerating_nonterminals(self.g)
        self.assertTrue(self.g.have_term([0, 1]))
        self.assertTrue(self.g.have_nonterm([A, B, C]))

    def test_partlyIncompleteTestWithChange(self):
        changed = ContextFree.remove_nongenerating_nonterminals(self.g, transform_grammar=True)
        self.assertEqual(id(changed), id(self.g))
        self.assertTrue(self.g.have_term([0, 1]))
        self.assertTrue(self.g.have_nonterm([A, B]))
        self.assertFalse(self.g.have_nonterm(C))


if __name__ == '__main__':
    main()
