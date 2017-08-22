#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 22.08.2017 21:14
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import main, TestCase
from grammpy import *
from grammpy_transforms import ContextFree


class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class C(Nonterminal): pass
class Rules(Rule):
    rules = [
        ([S], [0, B, 0]),
        ([S], [A]),
        ([A], [0, A]),
        ([A], [B]),
        ([B], [1, B]),
        ([B], [A, B]),
        ([B], [C]),
        ([B], [EPS]),
        ([C], [1, A]),
        ([C], [1])]

"""
 ---------------------------------
 |   S   |   A   |   B   |   C   |
----------------------------------
S|  []   |  [2]  | [2,4] |[2,4,7]|
----------------------------------
A|       |  []   |  [4]  | [4,7] |
----------------------------------
B|       |       |  []   |  [7]  |
----------------------------------
C|       |       |       |  []   |
----------------------------------
"""

class SimpleTest(TestCase):
    def test_simpleTest(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B, C],
                    rules=[Rules],
                    start_symbol=S)
        res = ContextFree.find_nonterminals_reachable_by_unit_rules(g)


if __name__ == '__main__':
    main()
