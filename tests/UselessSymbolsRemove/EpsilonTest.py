#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 19.08.2017 16:34
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import *

class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class C(Nonterminal): pass
class D(Nonterminal): pass
class Rules(Rule):
    rules = [
        ([S], [0, S]),
        ([S], [1, D]),
        ([S], [EPS]),
        ([A], [0, C, B]),
        ([A], [0, A, D]),
        ([B], [1, B]),
        ([B], [1, 1, 0]),
        ([C], [1, C, C]),
        ([C], [0, A, 1, B]),
        ([D], [1, 1, A]),
        ([D], [0, D, 0, 0]),
        ([D], [1, S]),
        ([D], [EPS])]

class SimpleTest(TestCase):
    def test_epsilonTest(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        self.assertEqual(g.rules_count(), 13)
        com = ContextFree.remove_useless_symbols(g)
        self.assertTrue(com.have_term([0, 1]))
        self.assertTrue(com.have_nonterm([S, D]))
        self.assertFalse(com.have_nonterm(A))
        self.assertFalse(com.have_nonterm(B))
        self.assertFalse(com.have_nonterm(C))
        self.assertEqual(com.rules_count(), 6)

    def test_epsilonTestShouldNotChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        self.assertEqual(g.rules_count(), 13)
        ContextFree.remove_useless_symbols(g)
        self.assertTrue(g.have_term([0, 1]))
        self.assertTrue(g.have_nonterm([S, A, B, C, D]))
        self.assertEqual(g.rules_count(), 13)

    def test_epsilonTestShouldChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        self.assertEqual(g.rules_count(), 13)
        ContextFree.remove_useless_symbols(g, transform_grammar=True)
        self.assertTrue(g.have_term([0, 1]))
        self.assertTrue(g.have_nonterm([S, D]))
        self.assertFalse(g.have_nonterm(A))
        self.assertFalse(g.have_nonterm(B))
        self.assertFalse(g.have_nonterm(C))
        self.assertEqual(g.rules_count(), 6)



if __name__ == '__main__':
    main()