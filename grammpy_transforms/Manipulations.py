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
    pass

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
