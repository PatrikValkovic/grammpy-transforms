#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 20.08.2017 15:43
:Licence GNUv3
Part of grammpy-transforms

"""

from copy import copy
from grammpy import Grammar, Rule, EPSILON
from .find_nonterminals_rewritable_to_epsilon import find_nonterminals_rewritable_to_epsilon


class EpsilonRemovedRule(Rule):
    """
    Represent rule, when one symbol of the original rule is rewritable to epsilon.
    """
    from_rule = None  # type: Rule
    replace_index = None  # type: int
    backtrack = None  # type: dict

def _create_rule(rule: Rule, index: int, backtrack: dict) -> EpsilonRemovedRule:
    """
    Create EpsilonRemovedRule
    :param rule: Original rule
    :param index: Index of symbol that is rewritable to epsilon
    :param backtrack: Dictionary where key is nonterminal and value is rule which is next to generate epsilon.
    :return: EpsilonRemovedRule class without symbol rewritable to epsilon
    """
    # Remove old rules
    old_dict = rule.__dict__.copy()
    if 'rules' in old_dict: del old_dict['rules']
    if 'rule' in old_dict: del old_dict['rule']
    if 'left' in old_dict: del old_dict['left']
    if 'right' in old_dict: del old_dict['right']
    if 'fromSymbol' in old_dict: del old_dict['fromSymbol']
    if 'toSymbol' in old_dict: del old_dict['toSymbol']
    # Create type
    created = type('NoEps'+rule.__name__, (EpsilonRemovedRule,), old_dict)
    # Add from_rule and index
    created.from_rule = rule
    created.replace_index = index
    created.backtrack = backtrack
    # Add rule
    created.fromSymbol = rule.fromSymbol
    created.right = [rule.right[i] for i in range(len(rule.right)) if i != index]
    if len(created.right) == 0:
        created.right = [EPSILON]
    return created

def remove_rules_with_epsilon(grammar: Grammar, transform_grammar=False) -> Grammar:
    """
    Remove epsilon rules.
    :param grammar: Grammar where rules remove
    :param transform_grammar: True if transformation should be performed in place, false otherwise.
    False by default.
    :return: Grammar without epsilon rules.
    """
    # Copy if required
    if transform_grammar is False: grammar = copy(grammar)
    # Find nonterminals rewritable to epsilon
    rewritable = find_nonterminals_rewritable_to_epsilon(grammar)
    # Create list from rules
    rules = list(grammar.rules())
    index = 0
    # Iterate thought rules
    while index < len(rules):
        rule = rules[index]
        index += 1
        right = rule.right
        if right == [EPSILON]:
            if not grammar.start_isSet() or rule.fromSymbol != grammar.start_get():
                grammar.remove_rule(rule)
            # Continue IS executed, but due optimalization line is marked as missed.
            continue #pragma: no cover
        for rule_index in range(len(right)):
            symbol = right[rule_index]
            if symbol in rewritable:
                new_rule = _create_rule(rule, rule_index, rewritable)
                rules.append(new_rule)
                grammar.add_rule(new_rule)
    return grammar
