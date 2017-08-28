#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 16:01
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import ContextFree

class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class C(Nonterminal): pass
class Rules(Rule):
    rules = [
        ([S], [1, B]),
        ([A], [1, B]),
        ([A], [EPS]),
        ([B], [EPS]),
        ([B], [1, C]),
        ([C], [1, 1])]


class SimpleTest(TestCase):
    def test_simpleTest(self):
        g = Grammar(terminals=[1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules])
        n = ContextFree.find_nonterminals_rewritable_to_epsilon(g)
        self.assertEqual(len(n), 2)
        for i in [A, B]:
            self.assertIn(i, n)




if __name__ == '__main__':
    main()
