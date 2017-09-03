#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 28.08.2017 15:29
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
class RuleS(Rule):
    rules = [([S], [A, B, C])]
class RuleA(Rule):
    rules = [([A], [B, C, S])]
class RuleB(Rule):
    rules = [([B], [C, S, A])]
class RuleS0(Rule): rule = ([S], [0])
class RuleA1(Rule): rule = ([A], [1])
class RuleB2(Rule): rule = ([B], [2])
class RuleC3(Rule): rule = ([C], [3])


"""
S
|-A
| ` 1
|-B
| |-C
| | `3
| |-S
| | |-A
| | | `1
| | |-B
| | | `2
| | `-C
| |   `3
| `-A
|   `1
`-C
  `3 
"""


class MoreRulesWithMultipleNonterminalsTest(TestCase):
    def test_transform(self):
        g = Grammar(terminals=[0, 1, 2, 3],
                    nonterminals=[S, A, B, C],
                    rules=[RuleS, RuleA, RuleB, RuleS0, RuleA1, RuleB2, RuleC3],
                    start_symbol=S)
        gr = ContextFree.transform_to_chomsky_normal_form(g)
        pars = cyk(gr, [1, 3, 1, 2, 3, 1, 3])
        trans = InverseContextFree.transform_from_chomsky_normal_form(pars)
        self.assertIsInstance(trans, S)
        self.assertIsInstance(trans.to_rule, RuleS)
        a = trans.to_rule.to_symbols[0]
        self.assertIsInstance(a, A)
        self.assertIsInstance(a.to_rule, RuleA1)
        self.assertIsInstance(a.to_rule.to_symbols[0], Terminal)
        self.assertEqual(a.to_rule.to_symbols[0].s, 1)
        b = trans.to_rule.to_symbols[1]
        self.assertIsInstance(b, B)
        self.assertIsInstance(b.to_rule, RuleB)
        c = b.to_rule.to_symbols[0]
        self.assertIsInstance(c, C)
        self.assertIsInstance(c.to_rule, RuleC3)
        self.assertIsInstance(c.to_rule.to_symbols[0], Terminal)
        self.assertEqual(c.to_rule.to_symbols[0].s, 3)
        s = b.to_rule.to_symbols[1]
        self.assertIsInstance(s, S)
        self.assertIsInstance(s.to_rule, RuleS)
        self.assertIsInstance(s.to_rule.to_symbols[0], A)
        self.assertIsInstance(s.to_rule.to_symbols[0].to_rule, RuleA1)
        self.assertIsInstance(s.to_rule.to_symbols[0].to_rule.to_symbols[0], Terminal)
        self.assertEqual(s.to_rule.to_symbols[0].to_rule.to_symbols[0].s, 1)
        self.assertIsInstance(s.to_rule.to_symbols[1], B)
        self.assertIsInstance(s.to_rule.to_symbols[1].to_rule, RuleB2)
        self.assertIsInstance(s.to_rule.to_symbols[1].to_rule.to_symbols[0], Terminal)
        self.assertEqual(s.to_rule.to_symbols[1].to_rule.to_symbols[0].s, 2)
        self.assertIsInstance(s.to_rule.to_symbols[2], C)
        self.assertIsInstance(s.to_rule.to_symbols[2].to_rule, RuleC3)
        self.assertIsInstance(s.to_rule.to_symbols[2].to_rule.to_symbols[0], Terminal)
        self.assertEqual(s.to_rule.to_symbols[2].to_rule.to_symbols[0].s, 3)
        self.assertIsInstance(b.to_rule.to_symbols[2], A)
        self.assertIsInstance(b.to_rule.to_symbols[2].to_rule, RuleA1)
        self.assertIsInstance(b.to_rule.to_symbols[2].to_rule.to_symbols[0], Terminal)
        self.assertEqual(b.to_rule.to_symbols[2].to_rule.to_symbols[0].s, 1)
        self.assertIsInstance(pars.to_rule.to_symbols[2], C)
        self.assertIsInstance(pars.to_rule.to_symbols[2].to_rule, RuleC3)
        self.assertIsInstance(pars.to_rule.to_symbols[2].to_rule.to_symbols[0], Terminal)
        self.assertEqual(pars.to_rule.to_symbols[2].to_rule.to_symbols[0].s, 3)



if __name__ == '__main__':
    main()
