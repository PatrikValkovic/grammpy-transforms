#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 28.08.2017 15:29
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
    rules = [([S], [A, B, C]),
             ([A], [B, C, S]),
             ([B], [C, S, A])]

class MoreRulesWithMultipleNonterminalsTest(TestCase):
    def test_transform(self):
        g = Grammar(nonterminals=[S, A, B, C],
                    rules=[Rules])
        com = ContextFree.transform_to_chomsky_normal_form(g)
        self.assertEqual(com.rules_count(), 6)
        self.assertEqual(len(com.rules()), 6)
        fromS = list(filter(lambda r: r.fromSymbol == S, com.rules()))[0]
        self.assertEqual(fromS.right[0], A)
        tempS = fromS.right[1]
        fromSTemp = list(filter(lambda r: r.right == [B, C], com.rules()))[0]
        self.assertEqual(tempS, fromSTemp.fromSymbol)
        fromA = list(filter(lambda r: r.fromSymbol == A, com.rules()))[0]
        self.assertEqual(fromA.right[0], B)
        tempA = fromA.right[1]
        fromATemp = list(filter(lambda r: r.right == [C, S], com.rules()))[0]
        self.assertEqual(tempA, fromATemp.fromSymbol)
        fromB = list(filter(lambda r: r.fromSymbol == B, com.rules()))[0]
        self.assertEqual(fromB.right[0], C)
        tempB = fromB.right[1]
        fromBTemp = list(filter(lambda r: r.right == [S, A], com.rules()))[0]
        self.assertEqual(tempB, fromBTemp.fromSymbol)
        self.assertEqual(com.nonterms_count(), 7)
        self.assertEqual(len(com.nonterms()), 7)

    def test_transformShouldNotChange(self):
        g = Grammar(nonterminals=[S, A, B, C],
                    rules=[Rules])
        ContextFree.transform_to_chomsky_normal_form(g)
        self.assertEqual(g.rules_count(), 3)
        self.assertEqual(len(g.rules()), 3)

    def test_transformShouldChange(self):
        g = Grammar(nonterminals=[S, A, B, C],
                    rules=[Rules])
        ContextFree.transform_to_chomsky_normal_form(g, transform_grammar=True)
        self.assertEqual(g.rules_count(), 6)
        self.assertEqual(len(g.rules()), 6)
        fromS = list(filter(lambda r: r.fromSymbol == S, g.rules()))[0]
        self.assertEqual(fromS.right[0], A)
        tempS = fromS.right[1]
        fromSTemp = list(filter(lambda r: r.right == [B, C], g.rules()))[0]
        self.assertEqual(tempS, fromSTemp.fromSymbol)
        fromA = list(filter(lambda r: r.fromSymbol == A, g.rules()))[0]
        self.assertEqual(fromA.right[0], B)
        tempA = fromA.right[1]
        fromATemp = list(filter(lambda r: r.right == [C, S], g.rules()))[0]
        self.assertEqual(tempA, fromATemp.fromSymbol)
        fromB = list(filter(lambda r: r.fromSymbol == B, g.rules()))[0]
        self.assertEqual(fromB.right[0], C)
        tempB = fromB.right[1]
        fromBTemp = list(filter(lambda r: r.right == [S, A], g.rules()))[0]
        self.assertEqual(tempB, fromBTemp.fromSymbol)
        self.assertEqual(g.nonterms_count(), 7)
        self.assertEqual(len(g.nonterms()), 7)

if __name__ == '__main__':
    main()
