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
class RuleAB(Rule): rule = ([A], [B])
class RuleAEps(Rule): rule = ([A], [EPS])
class RuleBEps(Rule): rule = ([B], [EPS])
class RuleB1C(Rule): rule = ([B], [2, C])
class RuleC11(Rule): rule = ([C], [3, 3])

"""
S->1B   A->1B   A->eps  B->eps  B->1C   C->11
ToEpsilon: A,B
S->1B   A->1B   A->eps  B->eps  B->1C   C->11   S->1    A->1
                ------  ------                  ++++    ++++
"""


class SimpleTestoverUnitRule(TestCase):
    def test_simpleTestOverUnitRule(self):
        g = Grammar(terminals=[0, 1, 2, 3],
                    nonterminals=[S, A, B, C],
                    rules=[RuleS0A, RuleAB, RuleAEps, RuleBEps, RuleB1C, RuleC11],
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
        self.assertIsInstance(a.to_rule, RuleAEps)
        self.assertIs(a.to_rule.to_symbols[0].s, EPS)


if __name__ == '__main__':
    main()
