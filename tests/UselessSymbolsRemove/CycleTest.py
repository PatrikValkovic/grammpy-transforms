#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 19.08.2017 16:13
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import main, TestCase
from grammpy import *
from grammpy_transforms import *

class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class C(Nonterminal): pass
class D(Nonterminal): pass
class Rules(Rule):
    rules = [([S], [A, B]),
             ([S], [C]),
             ([A], ['a', A]),
             ([A], ['a']),
             ([B], ['b', B]),
             ([C], ['c']),
             ([D], ['b', 'c'])]


class CycleTest(TestCase):
    def test_cycleTest(self):
        g = Grammar(terminals=['a', 'b', 'c'],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        self.assertEqual(g.rules_count(), 7)
        com = ContextFree.remove_useless_symbols(g)
        self.assertTrue(com.have_term('c'))
        self.assertFalse(com.have_term('a'))
        self.assertFalse(com.have_term('b'))
        self.assertTrue(com.have_nonterm([S, C]))
        self.assertFalse(com.have_nonterm(A))
        self.assertFalse(com.have_nonterm(B))
        self.assertFalse(com.have_nonterm(D))
        self.assertEqual(com.rules_count(), 2)

    def test_cycleTestShouldNotChange(self):
        g = Grammar(terminals=['a', 'b', 'c'],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        self.assertEqual(g.rules_count(), 7)
        ContextFree.remove_useless_symbols(g)
        self.assertTrue(g.have_term(['a', 'b', 'c']))
        self.assertTrue(g.have_nonterm([S, A, B, C, D]))
        self.assertEqual(g.rules_count(), 7)

    def test_cycleTestShouldChange(self):
        g = Grammar(terminals=['a', 'b', 'c'],
                    nonterminals=[S, A, B, C, D],
                    rules=[Rules],
                    start_symbol=S)
        self.assertEqual(g.rules_count(), 7)
        ContextFree.remove_useless_symbols(g, transform_grammar=True)
        self.assertTrue(g.have_term('c'))
        self.assertFalse(g.have_term('a'))
        self.assertFalse(g.have_term('b'))
        self.assertTrue(g.have_nonterm([S, C]))
        self.assertFalse(g.have_nonterm(A))
        self.assertFalse(g.have_nonterm(B))
        self.assertFalse(g.have_nonterm(D))
        self.assertEqual(g.rules_count(), 2)
