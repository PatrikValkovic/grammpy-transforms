#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 03.09.2017 19:05
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
class D(Nonterminal): pass
class RuleS1AB(Rule): rule=([S], [1, A, B])
class RuleB0(Rule): rule=([B], [0])
class RuleACD(Rule): rule=([A], [C, D])
class RuleCD(Rule): rule=([C], [D])
class RuleDEps(Rule): rule=([D], [EPS])


class SimpleTestoverUnitRule(TestCase):
    def test_simpleTestOverUnitRule(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C, D],
                    rules=[RuleS1AB, RuleB0, RuleACD, RuleCD, RuleDEps],
                    start_symbol=S)
        gr = ContextFree.transform_to_chomsky_normal_form(ContextFree.remove_unit_rules(ContextFree.remove_rules_with_epsilon(g)))
        pars = cyk(gr, [1, 0])
        s = InverseContextFree.epsilon_rules_restore(InverseContextFree.unit_rules_restore(InverseContextFree.transform_from_chomsky_normal_form(pars)))
        self.assertIsInstance(s, S)
        self.assertIsInstance(s.to_rule, RuleS1AB)
        self.assertIsInstance(s.to_rule.to_symbols[0], Terminal)
        self.assertEqual(s.to_rule.to_symbols[0].s, 1)
        b = s.to_rule.to_symbols[2]
        self.assertIsInstance(b, B)
        self.assertIsInstance(b.to_rule, RuleB0)
        self.assertIsInstance(b.to_rule.to_symbols[0], Terminal)
        self.assertEqual(b.to_rule.to_symbols[0].s, 0)
        a = s.to_rule.to_symbols[1]
        self.assertIsInstance(a, A)
        self.assertIsInstance(a.to_rule, RuleACD)
        d = a.to_rule.to_symbols[1]
        self.assertIsInstance(d, D)
        self.assertIsInstance(d.to_rule, RuleDEps)
        self.assertIs(d.to_rule.to_symbols[0].s, EPS)
        c = a.to_rule.to_symbols[0]
        self.assertIsInstance(c, C)
        self.assertIsInstance(c.to_rule, RuleCD)
        d = c.to_rule.to_symbols[0]
        self.assertIsInstance(d, D)
        self.assertIsInstance(d.to_rule, RuleDEps)
        self.assertIs(d.to_rule.to_symbols[0].s, EPS)


if __name__ == '__main__':
    main()

