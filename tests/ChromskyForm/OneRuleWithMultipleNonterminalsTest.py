#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 28.08.2017 14:37
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
    rules = [([S], [A,B,C])]

class OneRuleWithMultipleNonterminalsTest(TestCase):
    def test_transform(self):
        g = Grammar(nonterminals=[S, A, B, C],
                    rules=[Rules])
        com = ContextFree.transform_to_chomsky_normal_form(g)
        self.assertEqual(com.rules_count(), 2)
        self.assertEqual(len(com.rules()), 2)
        fromS = list(filter(lambda r: r.fromSymbol == S, com.rules()))[0]
        self.assertEqual(fromS.right[0], A)
        temp = fromS.right[1]
        fromTemp = list(filter(lambda r: r.right == [B, C], com.rules()))[0]
        self.assertEqual(temp, fromTemp.fromSymbol)
        self.assertEqual(com.nonterms_count(), 5)
        self.assertEqual(len(com.nonterms()), 5)

    def test_transformShouldNotChange(self):
        g = Grammar(nonterminals=[S, A,B,C],
                    rules=[Rules])
        ContextFree.transform_to_chomsky_normal_form(g)
        self.assertEqual(g.rules_count(), 1)
        self.assertEqual(len(g.rules()), 1)
        self.assertEqual(g.rules()[0], Rules)

    def test_transformShouldChange(self):
        g = Grammar(nonterminals=[S, A, B, C],
                    rules=[Rules])
        ContextFree.transform_to_chomsky_normal_form(g, transform_grammar=True)
        self.assertEqual(g.rules_count(), 2)
        self.assertEqual(len(g.rules()), 2)
        fromS = list(filter(lambda r: r.fromSymbol == S, g.rules()))[0]
        self.assertEqual(fromS.right[0], A)
        temp = fromS.right[1]
        fromTemp = list(filter(lambda r: r.right == [B, C], g.rules()))[0]
        self.assertEqual(temp, fromTemp.fromSymbol)
        self.assertEqual(g.nonterms_count(), 5)
        self.assertEqual(len(g.nonterms()), 5)





if __name__ == '__main__':
    main()