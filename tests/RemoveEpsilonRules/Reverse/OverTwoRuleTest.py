#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 16:01
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
class RuleS0A(Rule): rule = ([S], [0, A])
class RuleABC(Rule): rule = ([A], [B, C])
class RuleBC(Rule): rule = ([B], [C])
class RuleCEps(Rule): rule = ([C], [EPS])


class SimpleTestoverUnitRule(TestCase):
    def test_simpleTestOverUnitRule(self):
        g = Grammar(terminals=[0, 1, 2, 3],
                    nonterminals=[S, A, B, C],
                    rules=[RuleS0A, RuleABC, RuleBC, RuleCEps],
                    start_symbol=S)
        gr = ContextFree.transform_to_chomsky_normal_form(ContextFree.remove_unit_rules(ContextFree.remove_rules_with_epsilon(g)))
        pars = cyk(gr, [0])
        s = InverseContextFree.epsilon_rules_restore(InverseContextFree.unit_rules_restore(InverseContextFree.transform_from_chomsky_normal_form(pars)))
        self.assertIsInstance(s, S)
        self.assertIsInstance(s.to_rule, RuleS0A)
        self.assertIsInstance(s.to_rule.to_symbols[0], Terminal)
        self.assertEqual(s.to_rule.to_symbols[0].s, 0)
        a = s.to_rule.to_symbols[1]
        self.assertIsInstance(a, A)
        self.assertIsInstance(a.to_rule, RuleABC)
        c = a.to_rule.to_symbols[1]
        self.assertIsInstance(c, C)
        self.assertIsInstance(c.to_rule, RuleCEps)
        self.assertIs(c.to_rule.to_symbols[0].s, EPS)
        b = a.to_rule.to_symbols[0]
        self.assertIsInstance(b, B)
        self.assertIsInstance(b.to_rule, RuleBC)
        c = b.to_rule.to_symbols[0]
        self.assertIsInstance(c, C)
        self.assertIsInstance(c.to_rule, RuleCEps)
        self.assertIs(c.to_rule.to_symbols[0].s, EPS)


if __name__ == '__main__':
    main()
