#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 17.08.2017 14:39
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import ContextFree


class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class RuleSto0(Rule): rule = ([S], [0])
class RuleStoA(Rule): rule = ([S], [A])
class RuleAtoAB(Rule): rule = ([A], [A, B])
class RuleBto1(Rule): rule = ([B], [1])

class SimpleTest(TestCase):
    def test_simpleTest(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B],
                    rules=[RuleSto0, RuleStoA, RuleAtoAB, RuleBto1],
                    start_symbol=S)
        com = ContextFree.remove_useless_symbols(g)
        self.assertTrue(com.have_term(0))
        self.assertFalse(com.have_term(1))
        self.assertTrue(com.have_nonterm(S))
        self.assertFalse(com.have_nonterm(A))
        self.assertFalse(com.have_nonterm(B))

    def test_simpleTestShouldNotChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B],
                    rules=[RuleSto0, RuleStoA, RuleAtoAB, RuleBto1],
                    start_symbol=S)
        ContextFree.remove_useless_symbols(g)
        self.assertTrue(g.have_term([0, 1]))
        self.assertTrue(g.have_nonterm([S, A, B]))

    def test_simpleTestShouldChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B],
                    rules=[RuleSto0, RuleStoA, RuleAtoAB, RuleBto1],
                    start_symbol=S)
        ContextFree.remove_useless_symbols(g, transform_grammar=True)
        self.assertTrue(g.have_term(0))
        self.assertFalse(g.have_term(1))
        self.assertTrue(g.have_nonterm(S))
        self.assertFalse(g.have_nonterm(A))
        self.assertFalse(g.have_nonterm(B))



if __name__ == '__main__':
    main()