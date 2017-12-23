#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.12.2017 19:45
:Licence GNUv3
Part of grammpy-transforms

"""


from unittest import main, TestCase
from grammpy import *
from grammpy_transforms import *
from pyparsers import cyk


class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class Rules(Rule):
    rules = [
        ([S], [A, B]),
        ([A], [0]),
        ([B], [1])
    ]

class WithNonterminalsTest(TestCase):
    def test_parseWithNonterminal(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B],
                    rules=[Rules],
                    start_symbol=S)
        res = cyk(g, [0, 1])
        res = InverseCommon.splitted_rules(res)
        self.assertIsInstance(res, S)
        self.assertIsInstance(res.to_rule, Rules)
        a = res.to_rule.to_symbols[0]
        b = res.to_rule.to_symbols[1]
        self.assertIsInstance(a, A)
        self.assertIsInstance(b, B)
        self.assertIsInstance(a.to_rule, Rules)
        self.assertIsInstance(b.to_rule, Rules)


if __name__ == '__main__':
    main()