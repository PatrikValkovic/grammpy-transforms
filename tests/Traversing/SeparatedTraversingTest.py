#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 24.12.2017 11:57
:Licence GNUv3
Part of grammpy-transforms

"""
import functools, operator
from unittest import TestCase, main
from grammpy import *
from pyparsers import cyk
from grammpy_transforms import *


class A(Nonterminal): pass
class Rules(Rule):
    rule=([A], [0])


class SeparatedTraversingTest(TestCase):
    def testTraversingOwnTypes(self):
        g = Grammar(terminals=[0],
                    nonterminals=[A],
                    rules=[Rules],
                    start_symbol=A)
        res = cyk(g, [0])
        def travRule(item, callback):
            self.assertIsInstance(item, Rules)
        def travNonterminals(item, callback):
            self.assertIsInstance(item, A)
        def travTerms(item, callback):
            self.assertIsInstance(item, Terminal)
        Traversing.traverseSeparated(res, travRule, travNonterminals, travTerms)

    def testRealTraversing(self):
        g = Grammar(terminals=[0],
                    nonterminals=[A],
                    rules=[Rules],
                    start_symbol=A)
        res = cyk(g, [0])
        def travRule(item, callback):
            self.assertIsInstance(item, Rules)
            return [item] + [callback(ch) for ch in item.to_symbols]
        def travNonterminals(item, callback):
            self.assertIsInstance(item, A)
            return [item, callback(item.to_rule)]
        def travTerms(item, callback):
            self.assertIsInstance(item, Terminal)
            return [item]
        Traversing.traverseSeparated(res, travRule, travNonterminals, travTerms)


    def testRealTraversingReturnValues(self):
        g = Grammar(terminals=[0],
                    nonterminals=[A],
                    rules=[Rules],
                    start_symbol=A)
        res = cyk(g, [0])
        def travRule(item, callback):
            self.assertIsInstance(item, Rules)
            resp = [callback(ch) for ch in item.to_symbols]
            return functools.reduce(operator.add, resp, [item])
        def travNonterminals(item, callback):
            self.assertIsInstance(item, A)
            return [item] + callback(item.to_rule)
        def travTerms(item, callback):
            self.assertIsInstance(item, Terminal)
            return [item]
        resp = Traversing.traverseSeparated(res, travRule, travNonterminals, travTerms)
        self.assertIsInstance(resp[0], A)
        self.assertIsInstance(resp[1], Rules)
        self.assertIsInstance(resp[2], Terminal)
        self.assertEqual(resp[2].s, 0)



if __name__ == '__main__':
    main()
