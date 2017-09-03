#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 28.08.2017 14:37
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import ContextFree, InverseContextFree
from pyparsers import cyk

class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class C(Nonterminal): pass
class RuleSABC(Rule):
    rule = ([S], [A, B, C])
class RuleA0(Rule):
    rule = ([A], [0])
class RuleB1(Rule):
    rule = ([B], [1])
class RuleC2(Rule):
    rule = ([C], [2])

class OneRuleWithMultipleNonterminalsTest(TestCase):
    def test_transform(self):
        g = Grammar(terminals=[0, 1, 2],
                    nonterminals=[S, A, B, C],
                    rules=[RuleSABC, RuleA0, RuleB1, RuleC2],
                    start_symbol=S)
        com = ContextFree.transform_to_chomsky_normal_form(g)
        pars = cyk(com, [0, 1, 2])
        trans = InverseContextFree.transform_from_chomsky_normal_form(pars)
        self.assertIsInstance(trans, S)
        self.assertIsInstance(trans.to_rule, RuleSABC)
        a = trans.to_rule.to_symbols[0]
        b = trans.to_rule.to_symbols[1]
        c = trans.to_rule.to_symbols[2]
        self.assertIsInstance(a, A)
        self.assertIsInstance(a.to_rule, RuleA0)
        self.assertIsInstance(a.to_rule.to_symbols[0], Terminal)
        self.assertEqual(a.to_rule.to_symbols[0].s, 0)
        self.assertIsInstance(b, B)
        self.assertIsInstance(b.to_rule, RuleB1)
        self.assertIsInstance(b.to_rule.to_symbols[0], Terminal)
        self.assertEqual(b.to_rule.to_symbols[0].s, 1)
        self.assertIsInstance(c, C)
        self.assertIsInstance(c.to_rule, RuleC2)
        self.assertIsInstance(c.to_rule.to_symbols[0], Terminal)
        self.assertEqual(c.to_rule.to_symbols[0].s, 2)








if __name__ == '__main__':
    main()