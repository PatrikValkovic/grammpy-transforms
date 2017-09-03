#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 20:51
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import main, TestCase
from grammpy import *
from grammpy_transforms import ContextFree, InverseContextFree
from pyparsers import cyk


class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class C(Nonterminal): pass
class D(Nonterminal): pass
class RuleSA(Rule): rule=([S], [A])
class RuleSB(Rule): rule=([S], [B])
class RuleAC(Rule): rule=([A], [C])
class RuleA0A(Rule): rule=([A], [0, A])
class RuleA1S(Rule): rule=([A], [1, S])
class RuleBD(Rule): rule=([B], [D])
class RuleB2B(Rule): rule=([B], [2, B])
class RuleB3S(Rule): rule=([B], [3, S])
class RuleC1C(Rule): rule=([C], [1, C])
class RuleC0(Rule): rule=([C], [0])
class RuleD3D(Rule): rule=([D], [3, D])
class RuleD2(Rule): rule=([D], [2])

"""
 -------------------------------
 |  S  |  A  |  B  |  C  |  D  |
--------------------------------
S| []  | [1] | [2] |[1,3]|[2,6]|
--------------------------------
A|     | []  |     | [3] |     |
--------------------------------
B|     |     | []  |     | [6] |
--------------------------------
C|     |     |     | []  |     |
--------------------------------
D|     |     |     |     | []  |
--------------------------------

S->A  S->B  A->C  A->0A  A->1S  B->D  B->2B  B->3S  C->1C  C->0  D->3D  D->2
----  ----  ----                ----                         

S->A->0A
S->A->1S
S->A->C->1C
S->A->C->0
S->B->2B
S->B->3S
S->B->D->3D
S->B->D->2
A->C->1C
A->C->0
B->D->3D
B->D->2
"""


class SimpleTest(TestCase):
    def test_directTo2(self):
        g = Grammar(terminals=[0, 1, 2, 3],
                    nonterminals=[S, A, B, C, D],
                    rules=[RuleSA, RuleSB, RuleAC, RuleA0A, RuleA1S, RuleBD, RuleB2B,
                           RuleB3S, RuleC1C, RuleC0, RuleD3D, RuleD2],
                    start_symbol=S)
        gr = ContextFree.transform_to_chomsky_normal_form(ContextFree.remove_unit_rules(g))
        pars = cyk(gr, [2])
        s = InverseContextFree.unit_rules_restore(InverseContextFree.transform_from_chomsky_normal_form(pars))
        self.assertIsInstance(s, S)
        self.assertIsInstance(s.to_rule, RuleSB)
        b = s.to_rule.to_symbols[0]
        self.assertIsInstance(b, B)
        self.assertIsInstance(b.to_rule, RuleBD)
        d = b.to_rule.to_symbols[0]
        self.assertIsInstance(d, D)
        self.assertIsInstance(d.to_rule, RuleD2)
        self.assertIsInstance(d.to_rule.to_symbols[0], Terminal)
        self.assertEqual(d.to_rule.to_symbols[0].s, 2)

    def test_repeatOfC(self):
        g = Grammar(terminals=[0, 1, 2, 3],
                    nonterminals=[S, A, B, C, D],
                    rules=[RuleSA, RuleSB, RuleAC, RuleA0A, RuleBD, RuleB2B,
                           RuleB3S, RuleC1C, RuleC0, RuleD3D, RuleD2],
                    start_symbol=S)
        gr = ContextFree.transform_to_chomsky_normal_form(ContextFree.remove_unit_rules(g))
        pars = cyk(gr, [1, 1, 0])
        s = InverseContextFree.unit_rules_restore(InverseContextFree.transform_from_chomsky_normal_form(pars))
        self.assertIsInstance(s, S)
        self.assertIsInstance(s.to_rule, RuleSA)
        a = s.to_rule.to_symbols[0]
        self.assertIsInstance(a, A)
        self.assertIsInstance(a.to_rule, RuleAC)
        c = a.to_rule.to_symbols[0]
        self.assertIsInstance(c, C)
        self.assertIsInstance(c.to_rule, RuleC1C)
        self.assertIsInstance(c.to_rule.to_symbols[0], Terminal)
        self.assertEqual(c.to_rule.to_symbols[0].s, 1)
        c = c.to_rule.to_symbols[1]
        self.assertIsInstance(c, C)
        self.assertIsInstance(c.to_rule, RuleC1C)
        self.assertIsInstance(c.to_rule.to_symbols[0], Terminal)
        self.assertEqual(c.to_rule.to_symbols[0].s, 1)
        c = c.to_rule.to_symbols[1]
        self.assertIsInstance(c, C)
        self.assertIsInstance(c.to_rule, RuleC0)
        self.assertIsInstance(c.to_rule.to_symbols[0], Terminal)
        self.assertEqual(c.to_rule.to_symbols[0].s, 0)


if __name__ == '__main__':
    main()
