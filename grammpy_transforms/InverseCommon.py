#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.12.2017 16:03
:Licence GNUv3
Part of grammpy-transforms

"""

from .SplittedRules import splitted_rules

class InverseCommon:

    @staticmethod
    def splitted_rules(root):
        return splitted_rules(root)
