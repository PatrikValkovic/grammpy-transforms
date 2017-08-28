#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 15:55
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
class D(Nonterminal): pass
class Rules(Rule):
    rules = [
        ([S], [A, 0, A]),
        ([S], [0]),
        ([A], [B, C]),
        ([A], [2]),
        ([A], [C, C, C]), # multiple here
        ([B], [1, C]),
        ([B], [3, D]),
        ([B], [EPS]),
        ([C], [A, A, 3]),
        ([C], [EPS]),
        ([D], [A, A, B]),
        ([D], [A, A, 3])]


class MultipleUsageTest(TestCase):
    def test_multipleUsage(self):
        g = Grammar(terminals=[0,1,2,3],
                    nonterminals=[S,A,B,C, D],
                    rules=[Rules])
        n = ContextFree.find_nonterminals_rewritable_to_epsilon(g)
        self.assertEqual(len(n), 4)
        for i in [A, B, C, D]:
            self.assertIn(i, n)





if __name__ == '__main__':
    main()
