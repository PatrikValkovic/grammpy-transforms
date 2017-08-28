#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 28.08.2017 16:19
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import ContextFree


class S(Nonterminal): pass


class Rules(Rule):
    rules = [([S], [0, 1])]


class MoreRulesWithMultipleNonterminalsTest(TestCase):
    def test_transform(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S],
                    rules=[Rules])
        com = ContextFree.transform_to_chomsky_normal_form(g)
        self.assertEqual(com.rules_count(), 3)
        self.assertEqual(len(com.rules()), 3)
        fromS = list(filter(lambda r: r.fromSymbol == S, com.rules()))[0]
        to0 = fromS.right[0]
        to1 = fromS.right[1]
        self.assertTrue(issubclass(to0, ContextFree.ChomskyTermNonterminal))
        self.assertTrue(issubclass(to1, ContextFree.ChomskyTermNonterminal))
        to0R = list(filter(lambda r: r.right == [0], com.rules()))[0]
        to1R = list(filter(lambda r: r.right == [1], com.rules()))[0]
        self.assertEqual(to0R.fromSymbol, to0)
        self.assertEqual(to1R.fromSymbol, to1)
        self.assertEqual(com.nonterms_count(), 3)
        self.assertEqual(len(com.nonterms()), 3)

    def test_transformShouldNotChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S],
                    rules=[Rules])
        ContextFree.transform_to_chomsky_normal_form(g)
        self.assertEqual(g.rules_count(), 1)
        self.assertEqual(len(g.rules()), 1)
        self.assertEqual(g.rules()[0], Rules)

    def test_transformShouldChange(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S],
                    rules=[Rules])
        ContextFree.transform_to_chomsky_normal_form(g, transform_grammar=True)
        self.assertEqual(g.rules_count(), 3)
        self.assertEqual(len(g.rules()), 3)
        fromS = list(filter(lambda r: r.fromSymbol == S, g.rules()))[0]
        to0 = fromS.right[0]
        to1 = fromS.right[1]
        self.assertTrue(issubclass(to0, ContextFree.ChomskyTermNonterminal))
        self.assertTrue(issubclass(to1, ContextFree.ChomskyTermNonterminal))
        to0R = list(filter(lambda r: r.right == [0], g.rules()))[0]
        to1R = list(filter(lambda r: r.right == [1], g.rules()))[0]
        self.assertEqual(to0R.fromSymbol, to0)
        self.assertEqual(to1R.fromSymbol, to1)
        self.assertEqual(g.nonterms_count(), 3)
        self.assertEqual(len(g.nonterms()), 3)


if __name__ == '__main__':
    main()
