#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 28.08.2017 10:19
:Licence GNUv3
Part of grammpy-transforms

"""

from inspect import isclass
from copy import copy
from grammpy import *


class ChomskyNonterminal(Nonterminal):
    """
    Base class for all nonterminals used in Chomsky Normal Form
    """
    pass

class ChomskyGroupNonterminal(ChomskyNonterminal):
    """
    Class representing nonterminal that represents nonterminal tail when rule is splitted
    """
    group = []

class ChomskyTermNonterminal(ChomskyNonterminal):
    """
    Class representing nonterminal directly rewritable to terminal
    """
    for_term = None

class ChomskyRule(Rule):
    """
    Base class for all rules used in Chomsky Normal Form
    """
    pass

class ChomskySplitRule(ChomskyRule):
    """
    Class representing split rule with more than two nonterminals.
    First symbol of the right side is first symbol in the original rule.
    Second symbol of the right side is always ChomskyGroupNonterminal.
    """
    from_rule = None

class ChomskyRestRule(ChomskyRule):
    """
    Class representing rule for ChomskyGroupNonterminal class.
    """
    from_rule = None

class ChomskyTerminalReplaceRule(ChomskyRule):
    """
    Replacement of rule, that have two symbol on the right side, but one of it is terminal.
    """
    from_rule = None
    replaced_index = None

class ChomskyTermRule(ChomskyRule):
    """
    Rule that directly rewrite nonterminal to terminal.
    """
    pass

class Container:
    """
    Represent container that hold terminal, appropriate ChomskyTermNonterminal and ChomskyTermRule together.
    """
    def __init__(self, terminal, nonterminal, rule):
        """
        Create instance
        :param terminal: Terminal to be use
        :param nonterminal: Nonterminal directly rewritable to terminal
        :param rule: Rule that rewrite nonterminal to terminal
        """
        self.used = False
        self.terminal = terminal
        self.nonterminal = nonterminal
        self.rule = rule

class TerminalsFilling:
    """
    Store all terminals and their appropriate ChomskyTermNonterminal and ChomskyTermRule.
    Automatically add rule and nonterminal into grammar if used.
    """
    def __init__(self, grammar: Grammar):
        """
        :param grammar: Grammar to work with
        """
        self._grammar = grammar
        self._items = dict()
        self._counter = 0
        for term in grammar.terms():
            t = term.s
            created_nonterm = type("ChomskyNonterminalForTerm" + str(self._counter), (ChomskyTermNonterminal,), ChomskyTermNonterminal.__dict__.copy())
            created_nonterm.for_term = t
            created_rule = type("ChomskyRuleForTerm" + str(self._counter), (ChomskyTermRule,), ChomskyTermRule.__dict__.copy())
            created_rule.rule = ([created_nonterm], [t])
            self._items[t] = Container(term, created_nonterm, created_rule)
            self._counter += 1

    def get(self, term):
        """
        Get nonterminal rewritable to term.
        If needed, nonterminal and rule rewritable to terminal are added into grammar.
        :param term: Term for which get the nonterminal
        :return: ChomskyTermNonterminal class for terminal
        """
        if self._items[term].used is False:
            cont = self._items[term]
            self._grammar.add_nonterm(cont.nonterminal)
            self._grammar.add_rule(cont.rule)
            cont.used = True
        return self._items[term].nonterminal


def transform_to_chomsky_normal_form(grammar: Grammar, transform_grammar=False):
    """
    Transform grammar to Chomsky Normal Form
    :param grammar: Grammar to transform
    :param transform_grammar: True if transformation should be performed in place, false otherwise.
    False by default.
    :return: Grammar in Chomsky Normal Form.
    """
    # Copy if required
    if transform_grammar is False: grammar = copy(grammar)
    fill = TerminalsFilling(grammar)
    all_rules = grammar.rules()
    index = 0
    while index < len(all_rules):
        rule = all_rules[index]  # type: Rule
        index += 1
        #Check, if rule must be split
        if len(rule.right) > 2:
            grammar.remove_rule(rule)
            #create nonterm that represent group on the right
            created_nonterm = type("ChomskyGroupNonterminal"+str(index-1), (ChomskyGroupNonterminal,), ChomskyGroupNonterminal.__dict__.copy())
            created_nonterm.group = rule.right[1:]
            #create rule that replace current
            created_left_rule = type("ChomskySplitRule"+str(index-1), (ChomskySplitRule,), ChomskySplitRule.__dict__.copy())
            created_left_rule.rule = ([rule.fromSymbol], [rule.right[0], created_nonterm])
            created_left_rule.from_rule = rule
            #create rule with symbols on the right
            created_right_rule = type("ChomskySplitTempRule" + str(index - 1), (ChomskyRestRule,), ChomskyRestRule.__dict__.copy())
            created_right_rule.rule = ([created_nonterm], rule.right[1:])
            created_right_rule.from_rule = rule
            #fill
            grammar.add_nonterm(created_nonterm)
            grammar.add_rule([created_left_rule, created_right_rule])
            all_rules.append(created_left_rule)
            all_rules.append(created_right_rule)
        # Check, if must replace terminal
        elif len(rule.right) == 2:
            if grammar.have_term(rule.right[0]):
                #first symbol is terminal
                grammar.remove_rule(rule)
                symb = fill.get(rule.right[0])
                created = type("ChomskyLeftReplaceRule"+str(index-1), (ChomskyTerminalReplaceRule,), ChomskyTerminalReplaceRule.__dict__.copy())
                created.rule = ([rule.fromSymbol], [symb, rule.right[1]])
                created.from_rule = rule
                created.replaced_index = 0
                # fill it
                grammar.add_rule(created)
                all_rules.append(created)
            elif grammar.have_term(rule.right[1]):
                #second symbol is terminal
                grammar.remove_rule(rule)
                symb = fill.get(rule.right[1])
                created = type("ChomskyRightReplaceRule" + str(index - 1), (ChomskyTerminalReplaceRule,), ChomskyTerminalReplaceRule.__dict__.copy())
                created.rule = ([rule.fromSymbol], [rule.right[0], symb])
                created.from_rule = rule
                created.replaced_index = 1
                # fill it
                grammar.add_rule(created)
                all_rules.append(created)
    return grammar
