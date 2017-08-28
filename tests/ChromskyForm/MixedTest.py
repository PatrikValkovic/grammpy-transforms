#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 28.08.2017 19:49
:Licence GNUv3
Part of grammpy-transforms

"""


from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import ContextFree

class S(Nonterminal): pass
class A(Nonterminal): pass
class B(Nonterminal): pass
class Rules(Rule):
    rules = [([S], ['a', B]),
             ([S], ['b', A]),
             ([A], ['a', S]),
             ([A], ['b', A, A]),
             ([A], ['a']),
             ([B], [A, A]),
             ([B], ['a', B, B, 'a', A])]

"""
S->a'B | b'A
A->a'S | b'{AA} | a
B->AA | a'{BBaA}
{AA} -> AA
{BBaA} -> B{BaA}
{BaA} -> B{aA}
{aA} -> a'A
a' -> a
b' -> b
"""

class MoreRulesWithMultipleNonterminalsTest(TestCase):
    def test_transform(self):
        g = Grammar(terminals=['a', 'b'],
                    nonterminals=[S, A, B],
                    rules=[Rules])
        com = ContextFree.transform_to_chomsky_normal_form(g)
        self.assertEqual(com.rules_count(), 13)
        self.assertEqual(len(com.rules()), 13)
        self.assertEqual(com.nonterms_count(), 9)
        self.assertEqual(len(com.nonterms()), 9)
        # Old
        class AaRule(Rule): rule=([A], ['a'])
        self.assertTrue(com.have_rule(AaRule))
        class BAARule(Rule): rule=([B], [A, A])
        self.assertTrue(com.have_rule(BAARule))
        # New
        StoaB = list(filter(lambda r: r.fromSymbol == S and r.right[1] == B, com.rules()))[0]
        special_a = StoaB.right[0]
        StobA = list(filter(lambda r: r.fromSymbol == S and r.right[1] == A, com.rules()))[0]
        special_b = StobA.right[0]
        class StoaBRule(Rule): rule=([S], [special_a, B])
        self.assertTrue(com.have_rule(StoaBRule))
        class StobARule(Rule): rule=([S], [special_b, A])
        self.assertTrue(com.have_rule(StobARule))
        class AtoaSRule(Rule): rule=([A], [special_a, S])
        self.assertTrue(com.have_rule(AtoaSRule))
        AtobAA = list(filter(lambda r: r.fromSymbol == A and r.right[0] == special_b, com.rules()))[0]
        new_AA = AtobAA.right[1]
        class AtoabAARule(Rule): rule=([A], [special_b, new_AA])
        self.assertTrue(com.have_rule(AtoabAARule))
        BtoaBBaA = list(filter(lambda r: r.fromSymbol == B and r.right[0] == special_a, com.rules()))[0]
        new_BBaA = BtoaBBaA.right[1]
        class BtoaBBaA(Rule): rule=([B], [special_a, new_BBaA])
        self.assertTrue(com.have_rule(BtoaBBaA))
        class AAtoAARule(Rule): rule=([new_AA], [A, A])
        self.assertTrue(com.have_rule(AAtoAARule))
        BBaAtoBBaA = list(filter(lambda r: r.fromSymbol == new_BBaA, com.rules()))[0]
        self.assertEqual(BBaAtoBBaA.right[0], B)
        new_BaA = BBaAtoBBaA.right[1]
        BaAtoBaA = list(filter(lambda r: r.fromSymbol == new_BaA, com.rules()))[0]
        self.assertEqual(BaAtoBaA.right[0], B)
        new_aA = BaAtoBaA.right[1]
        class aAtoaARule(Rule): rule = ([new_aA], [special_a, A])
        self.assertTrue(com.have_rule(aAtoaARule))
        # Terminals
        class atoaRule(Rule): rule=([special_a], ['a'])
        self.assertTrue(com.have_rule(atoaRule))
        class btobRule(Rule): rule=([special_b], ['b'])
        self.assertTrue(com.have_rule(btobRule))

    def test_transformShouldNotChange(self):
        g = Grammar(terminals=['a', 'b'],
                    nonterminals=[S, A, B],
                    rules=[Rules])
        ContextFree.transform_to_chomsky_normal_form(g)
        self.assertEqual(g.rules_count(), 7)
        self.assertEqual(len(g.rules()), 7)
        self.assertEqual(g.nonterms_count(), 3)
        self.assertEqual(len(g.nonterms()), 3)
        self.assertTrue(g.have_rule(Rules))

    def test_transformShouldChange(self):
        g = Grammar(terminals=['a', 'b'],
                    nonterminals=[S, A, B],
                    rules=[Rules])
        ContextFree.transform_to_chomsky_normal_form(g, transform_grammar=True)
        self.assertEqual(g.rules_count(), 13)
        self.assertEqual(len(g.rules()), 13)
        self.assertEqual(g.nonterms_count(), 9)
        self.assertEqual(len(g.nonterms()), 9)
        # Old
        class AaRule(Rule): rule=([A], ['a'])
        self.assertTrue(g.have_rule(AaRule))
        class BAARule(Rule): rule=([B], [A, A])
        self.assertTrue(g.have_rule(BAARule))
        # New
        StoaB = list(filter(lambda r: r.fromSymbol == S and r.right[1] == B, g.rules()))[0]
        special_a = StoaB.right[0]
        StobA = list(filter(lambda r: r.fromSymbol == S and r.right[1] == A, g.rules()))[0]
        special_b = StobA.right[0]
        class StoaBRule(Rule): rule=([S], [special_a, B])
        self.assertTrue(g.have_rule(StoaBRule))
        class StobARule(Rule): rule=([S], [special_b, A])
        self.assertTrue(g.have_rule(StobARule))
        class AtoaSRule(Rule): rule=([A], [special_a, S])
        self.assertTrue(g.have_rule(AtoaSRule))
        AtobAA = list(filter(lambda r: r.fromSymbol == A and r.right[0] == special_b, g.rules()))[0]
        new_AA = AtobAA.right[1]
        class AtoabAARule(Rule): rule=([A], [special_b, new_AA])
        self.assertTrue(g.have_rule(AtoabAARule))
        BtoaBBaA = list(filter(lambda r: r.fromSymbol == B and r.right[0] == special_a, g.rules()))[0]
        new_BBaA = BtoaBBaA.right[1]
        class BtoaBBaA(Rule): rule=([B], [special_a, new_BBaA])
        self.assertTrue(g.have_rule(BtoaBBaA))
        class AAtoAARule(Rule): rule=([new_AA], [A, A])
        self.assertTrue(g.have_rule(AAtoAARule))
        BBaAtoBBaA = list(filter(lambda r: r.fromSymbol == new_BBaA, g.rules()))[0]
        self.assertEqual(BBaAtoBBaA.right[0], B)
        new_BaA = BBaAtoBBaA.right[1]
        BaAtoBaA = list(filter(lambda r: r.fromSymbol == new_BaA, g.rules()))[0]
        self.assertEqual(BaAtoBaA.right[0], B)
        new_aA = BaAtoBaA.right[1]
        class aAtoaARule(Rule): rule = ([new_aA], [special_a, A])
        self.assertTrue(g.have_rule(aAtoaARule))
        # Terminals
        class atoaRule(Rule): rule=([special_a], ['a'])
        self.assertTrue(g.have_rule(atoaRule))
        class btobRule(Rule): rule=([special_b], ['b'])
        self.assertTrue(g.have_rule(btobRule))



if __name__ == '__main__':
    main()
