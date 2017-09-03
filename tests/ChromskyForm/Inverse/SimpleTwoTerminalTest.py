#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 28.08.2017 16:19
:Licence GNUv3
Part of grammpy-transforms

"""

from unittest import TestCase, main
from grammpy import *
from grammpy_transforms import ContextFree, InverseContextFree
from pyparsers import cyk


class S(Nonterminal): pass
class Rules(Rule):
    rules = [([S], [0, 1])]


class MoreRulesWithMultipleNonterminalsTest(TestCase):
    def test_transform(self):
        g = Grammar(terminals=[0, 1],
                    nonterminals=[S],
                    rules=[Rules],
                    start_symbol=S)
        tr = ContextFree.transform_to_chomsky_normal_form(g)
        pars = cyk(tr, [0, 1])
        rest = InverseContextFree.transform_from_chomsky_normal_form(pars)
        self.assertIsInstance(rest, S)
        self.assertIsInstance(rest.to_rule, Rules)
        self.assertIsInstance(rest.to_rule.to_symbols[0], Terminal)
        self.assertIsInstance(rest.to_rule.to_symbols[1], Terminal)
        self.assertEqual(rest.to_rule.to_symbols[0].s, 0)
        self.assertEqual(rest.to_rule.to_symbols[1].s, 1)


if __name__ == '__main__':
    main()
