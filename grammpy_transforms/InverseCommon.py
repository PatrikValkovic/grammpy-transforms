#!/usr/bin/env python
"""
:Author Patrik Valkovic
:Created 23.12.2017 16:03
:Licence GNUv3
Part of grammpy-transforms

"""

from .SplittedRules import splitted_rules

class InverseCommon:
    """
    Class that associate functions transforming common AST.
    """

    @staticmethod
    def splitted_rules(root):
        """
        Replace SplittedRules by their original rule.
        :param root: Root of the AST
        :return: Modified AST
        """
        # TODO should by automatically
        return splitted_rules(root)
