#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 17.08.2017 14:23
:Licence GNUv3
Part of grammpy-transforms

"""


from unittest import main, TestCase
from grammpy import *
from grammpy_transforms import *


class A(Nonterminal): pass
class B(Nonterminal): pass
class C(Nonterminal): pass
class D(Nonterminal): pass
class E(Nonterminal): pass
class F(Nonterminal): pass
class RuleAto0B(Rule): rule = ([A], [0, B])
class RuleBto1C(Rule): rule = ([B], [1, C])
class RuleCto2C(Rule): rule = ([C], [2, C])




class RemovingTerminalsTest(TestCase):
    def test_removingTerminals(self):
        g = Grammar(terminals=[0, 1, 2, 3],
                    nonterminals=[A, B, C, D, E, F],
                    rules=[RuleAto0B, RuleBto1C, RuleCto2C],
                    start_symbol=A)
        com = ContextFree.remove_unreachable_symbols(g)
        self.assertTrue(com.have_term([0, 1, 2]))
        self.assertFalse(com.have_term(3))
        self.assertTrue(com.have_nonterm([A, B, C]))
        self.assertFalse(com.have_nonterm(D))
        self.assertFalse(com.have_nonterm(E))
        self.assertFalse(com.have_nonterm(F))

    def test_removingTerminalsShouldNotChange(self):
        g = Grammar(terminals=[0, 1, 2, 3],
                    nonterminals=[A, B, C, D, E, F],
                    rules=[RuleAto0B, RuleBto1C, RuleCto2C],
                    start_symbol=A)
        ContextFree.remove_unreachable_symbols(g)
        self.assertTrue(g.have_term([0, 1, 2, 3]))
        self.assertTrue(g.have_nonterm([A, B, C, D, E, F]))

    def test_removingTerminalsShouldChange(self):
        g = Grammar(terminals=[0, 1, 2, 3],
                    nonterminals=[A, B, C, D, E, F],
                    rules=[RuleAto0B, RuleBto1C, RuleCto2C],
                    start_symbol=A)
        ContextFree.remove_unreachable_symbols(g, transform_grammar=True)
        self.assertTrue(g.have_term([0, 1, 2]))
        self.assertFalse(g.have_term(3))
        self.assertTrue(g.have_nonterm([A, B, C]))
        self.assertFalse(g.have_nonterm(D))
        self.assertFalse(g.have_nonterm(E))
        self.assertFalse(g.have_nonterm(F))


if __name__ == '__main__':
    main()
