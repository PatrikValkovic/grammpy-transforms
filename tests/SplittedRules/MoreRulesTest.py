#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.12.2017 19:51
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
class AtoAB(Rule):
    rules = [([A], [A, B])]
class Rules(Rule):
    rules = [
        ([S], [A, B]),
        ([A], [0]),
        ([B], [1])
    ]

class WithNonterminalsTest(TestCase):
    def test_parseWithNoIteration(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B],
                    rules=[Rules, AtoAB],
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

    def test_parseWithOneIteration(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B],
                    rules=[Rules, AtoAB],
                    start_symbol=S)
        res = cyk(g, [0, 1, 1])
        res = InverseCommon.splitted_rules(res)
        self.assertIsInstance(res, S)
        self.assertIsInstance(res.to_rule, Rules)
        a = res.to_rule.to_symbols[0]
        b = res.to_rule.to_symbols[1]
        self.assertIsInstance(a, A)
        self.assertIsInstance(b, B)
        self.assertIsInstance(a.to_rule, AtoAB)
        self.assertIsInstance(b.to_rule, Rules)
        b = a.to_rule.to_symbols[1]
        a = a.to_rule.to_symbols[0]
        self.assertIsInstance(a, A)
        self.assertIsInstance(b, B)
        self.assertIsInstance(a.to_rule, Rules)
        self.assertIsInstance(b.to_rule, Rules)

    def test_parseWithThreeIterations(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S, A, B],
                    rules=[Rules, AtoAB],
                    start_symbol=S)
        res = cyk(g, [0, 1, 1, 1, 1])
        res = InverseCommon.splitted_rules(res)
        self.assertIsInstance(res, S)
        self.assertIsInstance(res.to_rule, Rules)
        a = res.to_rule.to_symbols[0]
        b = res.to_rule.to_symbols[1]
        self.assertIsInstance(a, A)
        self.assertIsInstance(b, B)
        self.assertIsInstance(a.to_rule, AtoAB)
        self.assertIsInstance(b.to_rule, Rules)
        b = a.to_rule.to_symbols[1]
        a = a.to_rule.to_symbols[0]
        self.assertIsInstance(a, A)
        self.assertIsInstance(b, B)
        self.assertIsInstance(a.to_rule, AtoAB)
        self.assertIsInstance(b.to_rule, Rules)
        b = a.to_rule.to_symbols[1]
        a = a.to_rule.to_symbols[0]
        self.assertIsInstance(a, A)
        self.assertIsInstance(b, B)
        self.assertIsInstance(a.to_rule, AtoAB)
        self.assertIsInstance(b.to_rule, Rules)
        b = a.to_rule.to_symbols[1]
        a = a.to_rule.to_symbols[0]
        self.assertIsInstance(a, A)
        self.assertIsInstance(b, B)
        self.assertIsInstance(a.to_rule, Rules)
        self.assertIsInstance(b.to_rule, Rules)


if __name__ == '__main__':
    main()