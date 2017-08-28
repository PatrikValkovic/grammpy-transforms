#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 16:07
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
        ([S], [0, A]),
        ([S], [1, C]),
        ([S], [C, C]),
        ([A], [B]),
        ([B], [S]),
        ([B], [EPS]),
        ([C], [A]),
        ([C], [S])]


class SimpleChainingTest(TestCase):
    def test_simpleChainingTest(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules])
        n = ContextFree.find_nonterminals_rewritable_to_epsilon(g)
        self.assertEqual(len(n), 4)
        for i in [S, A, B, C]:
            self.assertIn(i, n)




if __name__ == '__main__':
    main()
