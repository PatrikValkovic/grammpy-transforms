#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 24.12.2017 14:52
:Licence GNUv3
Part of grammpy-transforms

"""


from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import *


class A(Nonterminal): pass
class B(Nonterminal): pass

class ReplacingTest(TestCase):
    def testReplaceWithoutTest(self):
        a = A()
        b = B()
        Manipulations.replace(a, b)

    def testReplaceBottom(self):
        class S(Nonterminal): pass
        class R(Rule):
            rule=([S],[A])
        r = R()
        a = A()
        b = B()
        r.to_symbols.append(a)
        a._set_from_rule(r)
        self.assertIsNone(a.to_rule)
        Manipulations.replace(a, b)
        self.assertEqual(b.from_rule, r)
        self.assertIsNone(b.to_rule)
        self.assertEqual(r.to_symbols[0], b)

    def testReplaceTop(self):
        class S(Nonterminal): pass
        class R(Rule):
            rule=([S], [A])
        r = R()
        a = A()
        b = B()
        a._set_to_rule(r)
        r._from_symbols.append(a)
        self.assertIsNone(a.from_rule)
        Manipulations.replace(a, b)
        self.assertEqual(b.to_rule, r)
        self.assertIsNone(b.from_rule)
        self.assertEqual(r.from_symbols[0], b)

    def testReplaceMiddle(self):
        class S(Nonterminal): pass
        class R(Rule):
            rule=([S], [A])
        r1 = R()
        r2 = R()
        a = A()
        b = B()
        r1._to_symbols.append(a)
        a._set_from_rule(r1)
        a._set_to_rule(r2)
        r2._from_symbols.append(a)
        Manipulations.replace(a, b)
        self.assertEqual(b.from_rule, r1)
        self.assertEqual(b.to_rule, r2)
        self.assertEqual(r1.to_symbols[0], b)
        self.assertEqual(r2.from_symbols[0], b)

if __name__ == '__main__':
    main()
