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


class A(Nonterminal): pass
class B(Nonterminal): pass
class C(Nonterminal): pass
class D(Nonterminal): pass
class E(Nonterminal): pass


class IsGrammarGeneratingTest(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.g = Grammar()

    def setUp(self):
        self.g = Grammar(terminals=[0, 1, 2],
                         nonterminals=[A, B, C, D, E],
                         start_symbol=A)

    def test_allRulesGenerates(self):
        class RuleAto0B(Rule): rule = ([A], [0, B])
        class RuleBto1C(Rule): rule = ([B], [1, C])
        class RuleCto01(Rule): rule = ([C], [0, 1])
        self.g.add_rule([RuleAto0B,RuleBto1C, RuleCto01])
        self.assertTrue(ContextFree.is_grammar_generating(self.g))

    def test_allRulesGeneratesCycle(self):
        class RuleAto0B(Rule): rule = ([A], [0, B])
        class RuleBto1C(Rule): rule = ([B], [1, C])
        class RuleCto0C(Rule): rule = ([C], [0, C])
        class RuleCto1D(Rule): rule = ([C], [1, D])
        class RuleDto0011(Rule): rule = ([D], [0, 0, 1, 1])
        self.g.add_rule([RuleAto0B,RuleBto1C, RuleCto0C, RuleCto1D, RuleDto0011])
        self.assertTrue(ContextFree.is_grammar_generating(self.g))

    def test_grammarNotGenerate(self):
        class RuleAto0B(Rule): rule = ([A], [0, B])
        class RuleBto1C(Rule): rule = ([B], [1, C])
        self.g.add_rule([RuleAto0B,RuleBto1C])
        self.assertFalse(ContextFree.is_grammar_generating(self.g))

    def test_grammarNotGenerateCycle(self):
        class RuleAto0B(Rule): rule = ([A], [0, B])
        class RuleBto1C(Rule): rule = ([B], [1, C])
        class RuleCto0C(Rule): rule = ([C], [0, C])
        class RuleDto0011(Rule): rule = ([D], [0, 0, 1, 1])
        self.g.add_rule([RuleAto0B,RuleBto1C, RuleCto0C, RuleDto0011])
        self.assertFalse(ContextFree.is_grammar_generating(self.g))

    def test_grammarPartlyGenerate(self):
        class RuleAto0B(Rule): rule = ([A], [0, B])
        class RuleBto1C(Rule): rule = ([B], [1, C])
        class RuleBTo1D(Rule): rule = ([B], [1, D])
        class RuleCto1E(Rule): rule = ([C], [1, E])
        class RuleDto0011(Rule): rule = ([D], [0, 0, 1, 1])
        self.g.add_rule([RuleAto0B,RuleBto1C, RuleBTo1D, RuleCto1E, RuleDto0011])
        self.assertTrue(ContextFree.is_grammar_generating(self.g))

    def test_grammarPartlyGenerateCycle(self):
        class RuleAto0B(Rule): rule = ([A], [0, B])
        class RuleBto1C(Rule): rule = ([B], [1, C])
        class RuleBTo1D(Rule): rule = ([B], [1, D])
        class RuleCto1C(Rule): rule = ([C], [1, C])
        class RuleDto0011(Rule): rule = ([D], [0, 0, 1, 1])
        self.g.add_rule([RuleAto0B,RuleBto1C, RuleBTo1D, RuleCto1C, RuleDto0011])
        self.assertTrue(ContextFree.is_grammar_generating(self.g))


if __name__ == '__main__':
    main()
