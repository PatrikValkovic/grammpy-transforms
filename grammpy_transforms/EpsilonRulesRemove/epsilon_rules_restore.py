#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 03.09.2017 10:47
:Licence GNUv3
Part of grammpy-transforms

"""

from grammpy import *
from .remove_rules_with_epsilon import EpsilonRemovedRule
from ..Manipulations import Manipulations, Traversing


def _restore_tree_for(root: Nonterminal, translate: dict):
    if root is EPSILON:
        return Terminal(EPSILON, None)
    created_nonterm = root()  # type: Nonterminal
    created_rule = translate[root]()  # type: Rule
    created_nonterm._set_to_rule(created_rule)
    created_rule._from_symbols.append(created_nonterm)
    for ch in created_rule.right:
        p = _restore_tree_for(ch, translate)  # type: Nonterminal
        p._set_from_rule(created_rule)
        created_rule._to_symbols.append(p)
    return created_nonterm

def epsilon_rules_restore(root: Nonterminal):
    items = Traversing.postOrder(root)
    items = filter(lambda x: isinstance(x, EpsilonRemovedRule), items)
    for rule in items:
        created_rule = rule.from_rule()  # type: Rule
        #Solve parents
        for s in rule.from_symbols:  # type: Nonterminal
            s._set_to_rule(created_rule)
            created_rule._from_symbols.append(s)
        #Copy childs to replace index
        for i in range(rule.replace_index):
            ch = rule.to_symbols[i]  # type: Nonterminal
            ch._set_from_rule(created_rule)
            created_rule._to_symbols.append(ch)
        #Add epsilon
        symb = _restore_tree_for(created_rule.right[rule.replace_index], rule.backtrack) # type: Nonterminal
        created_rule._to_symbols.append(symb)
        if symb is not EPSILON:
            symb._set_from_rule(created_rule)
        #Add rest of childs
        for i in range(rule.replace_index, len(rule.to_symbols)):
            ch = rule.to_symbols[i]  # type: Nonterminal
            ch._set_from_rule(created_rule)
            created_rule._to_symbols.append(ch)
    return root
