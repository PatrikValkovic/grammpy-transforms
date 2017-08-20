#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 15:48
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
        ([S], [A, B, C]),
        ([A], [0, A]),
        ([A], [EPS]),
        ([B], [A]),
        ([B], [1, 1]),
        ([B], [EPS]),
        ([C], [EPS])]

"""
S->ABC  A->0A   A->eps  B->A    B->11   B->eps  C->eps
ToEpsilon: S,A,B,C
S->ABC  A->0A   A->eps  B->A    B->11   B->eps  C->eps  S->BC   S->AC   S->BC   
                ------                  ------  ------  +++++   +++++   +++++

A->0    S->B    S->C    S->A    S->eps
++++    ++++    ++++    ++++    ++++++
"""


class SimpleChainingTest(TestCase):
    def test_simpleChainingTest(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules])
        n = ContextFree.find_terminals_rewritable_to_epsilon(g)
        self.assertEqual(len(n), 4)
        for i in [S, A, B, C]:
            self.assertIn(i, n)




if __name__ == '__main__':
    main()
