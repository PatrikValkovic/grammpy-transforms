#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 24.12.2017 11:31
:Licence GNUv3
Part of grammpy-transforms

"""
import functools
import operator
from typing import Callable

from grammpy import Rule, Nonterminal, Terminal


class Manipulations:
    @staticmethod
    def replaceRule(oldRule: Rule, newRule: Rule) -> Rule:
        for par in oldRule.from_symbols:
            par._set_to_rule(newRule)
            newRule._from_symbols.append(par)
        for ch in oldRule.to_symbols:
            ch._set_from_rule(newRule)
            newRule._to_symbols.append(ch)
        return newRule

    @staticmethod
    def replaceNode(oldNode: Nonterminal, newNode: Nonterminal):
        if oldNode.from_rule is not None and len(oldNode.from_rule.to_symbols) > 0:
            indexParent = oldNode.from_rule.to_symbols.index(oldNode)
            oldNode.from_rule.to_symbols[indexParent] = newNode
            newNode._set_from_rule(oldNode.from_rule)
        if oldNode.to_rule is not None and len(oldNode.to_rule.from_symbols) > 0:
            indexChild = oldNode.to_rule.from_symbols.index(oldNode)
            oldNode.to_rule._from_symbols[indexChild] = newNode
            newNode._set_to_rule(oldNode.to_rule)
        return newNode

    @staticmethod
    def replace(oldEl, newEl):
        if isinstance(oldEl, Rule):
            return Manipulations.replaceRule(oldEl, newEl)
        if isinstance(oldEl, (Nonterminal, Terminal)):
            return Manipulations.replaceNode(oldEl, newEl)

class Traversing:
    @staticmethod
    def traverse(root, callback: Callable):
        def innerCallback(item):
            return callback(item, innerCallback)
        return callback(root, innerCallback)

    @staticmethod
    def traverseSeparated(root, callbackRules, callbackNonterminals, callbackTerminals):
        def separateTraverse(item, callback):
            if isinstance(item, Rule):
                return callbackRules(item, callback)
            if isinstance(item, Nonterminal):
                return callbackNonterminals(item, callback)
            if isinstance(item, Terminal):
                return callbackTerminals(item, callback)
        return Traversing.traverse(root, separateTraverse)

    @staticmethod
    def preOrder(root):
        def travRule(item, callback):
            resp = [callback(ch) for ch in item.to_symbols]
            return functools.reduce(operator.add, resp, [item])
        def travNonterminals(item, callback):
            return [item] + callback(item.to_rule)
        def travTerms(item, callback):
            return [item]
        return Traversing.traverseSeparated(root, travRule, travNonterminals, travTerms)

    @staticmethod
    def postOrder(root):
        def travRule(item, callback):
            resp = [callback(ch) for ch in item.to_symbols]
            return functools.reduce(operator.add, resp, []) + [item]
        def travNonterminals(item, callback):
            return callback(item.to_rule) + [item]
        def travTerms(item, callback):
            return [item]
        return Traversing.traverseSeparated(root, travRule, travNonterminals, travTerms)

    @staticmethod
    def print(root, previous=0, defined = [], is_last = False):
        ret = ''

        if previous != 0:
            for i in range(previous-1):
                if i in defined:
                    ret += '|  '
                else:
                    ret += '   '
            ret += '`--' if is_last else '|--';

        if isinstance(root, Nonterminal):
            ret += '(N)' + root.__class__.__name__ + '\n'
            ret += Traversing.print(root.to_rule, previous+1, defined, True)
        elif isinstance(root, Terminal):
            ret += '(T)' +str(root.s) + '\n'
            return ret
        elif isinstance(root, Rule):
            ret += '(R)' +root.__class__.__name__ + '\n'
            defined.append(previous)
            for i in range(len(root.to_symbols)-1):
                ret += Traversing.print(root.to_symbols[i],
                                        previous+1,
                                        defined,
                                        False)
            defined.pop()
            ret += Traversing.print(root.to_symbols[-1],
                                    previous + 1,
                                    defined,
                                    True)
        return ret