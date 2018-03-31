# grammpy [![Build Status](https://travis-ci.org/PatrikValkovic/grammpy-transforms.svg?branch=dev)](https://travis-ci.org/PatrikValkovic/grammpy-transforms) [![Coverage Status](https://coveralls.io/repos/github/PatrikValkovic/grammpy-transforms/badge.svg?branch=dev)](https://coveralls.io/github/PatrikValkovic/grammpy-transforms?branch=dev)

Package for transforming grammpy grammars. 

Currently only small subset of operations are implement.

Subset of methods for each type of grammar will be stored in separate object (currently only ContextFree is supported).

For each method, you can decide to modify or copy the grammar. Default behaviour is to copy grammar before each modification.
You can disable it for every method by passing `transform_grammar=True` as parameter.


## Regular grammars

Not implemented.

## Context-Free grammars

Only methods allowing to transform grammar into Chomsky normal form.

#### Removing of useless symbols

Including removing of unreachable symbols and symbols, thats not generate.

```python
from grammpy_transforms import ContextFree

new_g = ContextFree.remove_unreachable_symbols(g)
new_g = ContextFree.remove_nongenerating_nonterminals(g)
new_g = ContextFree.remove_useless_symbols(g)
ContextFree.is_grammar_generating(g)
```

#### Epsilon rules elimination

Method create new rules that will replace rules with nonterminal rewritable to epsilon rule.
You can also only search  for nonterminals, that are in rule with epsilon on the right side.

```python
from grammpy import *
from grammpy_transforms import ContextFree

class OldRules(Rule):
    rules = [([A], [B, C]), ([B], [EPS])]

ContextFree.find_nonterminals_rewritable_to_epsilon(g) # list of nonterminals
new_g = ContextFree.remove_rules_with_epsilon(g)

class NewRules(Rule):
    rules = [([A], [B, C]), ([A], [C])]
    
assert new_g.have_rule(NewRules) is True
```

Library creating own type of rule, so you can backtrack the changes.
The type is `ContextFree.EpsilonRemovedRule`.

```python
class CreatedRule(Rule):
    rule = ([A], [C])

created = new_g.get_rule(CreatedRule)
assert created.from_rule.rule == ([A], [B, C])
assert created.replace_index == 0
assert issubclass(created, ContextFree.EpsilonRemovedRule)
```

#### Removing of unit rules

As with epsilon rules removing, method for removing unit rules create new ones as so as removing invalid ones.
You can transform the grammar or just find reachable symbols.

```python
from grammpy import *
from grammpy_transforms import ContextFree

class OldRules(Rule):
    rules = [([A], [B]), ([B], [C]), ([B], [0]), ([C], [1])]

reach = ContextFree.find_nonterminals_reachable_by_unit_rules(g) # instance of ContextFree.UnitSymbolRechablingResults
assert reach.reach(A, B) is True
assert reach.reachables(A) == [A, B, C]
path = reach.path_rules(B, C) # list of unit rules
assert path[0].rule == ([B], [C])

new_g = ContextFree.remove_unit_rules(g)

class NewRules(Rule):
    rules = [([A], [0]), ([A], [1]), ([B], [0]), ([C], [1])]
    
assert new_g.have_rule(NewRules) is True
```

Method creates own type of rule (`ContextFree.ReducedUnitRule`) and you can backtrack the tranformations.

```python
class Ato1Rule(Rule): 
    rule=([A], [1])

created = new_g.get_rule(Ato1Rule)
assert created.by_rules[0].rule == ([A], [B])
assert created.by_rules[1].rule == ([B], [C])
assert created.end_rule.rule == ([C], [1])
```

#### Transformation to Chomsky normal form

Method transfer grammar into Chomsky normal form.

This operations create a lot of own types to allow easy backtracking of transformations.

Base classes are `ContextFree.ChomskyNonterminal` and `ContextFree.ChomskyRule`, that are base classes for other.

As nonterminals method use `ContextFree.ChomskyTermNonterminal` that represent nonterminal rewritable to terminal (A->a). Nonterminal have property `for_term`, where it stores terminal (as Terminal class).
Second class is `ContextFree.ChomskyGroupNonterminal`, that represent group of symbols (for example in rule A->BCD will this nonterminal represent CD). This nonterminal have property `group`, where it stores list of symbols, that represent.

For rules method create list of classes, where each class have different meaning:
- `ContextFree.ChomskySplitRule`: Represent rule, that was split to contain only two symbols. In property `from_rule` is stored original rule.
- `ContextFree.ChomskyRestRule`: Represent right part after splitting of rule. As previous, in `from_rule` property is stored original rule. 
When splitting, ChomskySplitRule and ChomskyRestRule represent original whole rule: `A->BCDE ==> A->BX and X->CDE`.
- `ContextFree.ChomskyTerminalReplaceRule`: This class is used in situations, where rule contains nonterminal with terminal. Rule is transformed into state, where terminal is replace with nonterminal rewritable to that terminal.
Class have `from_rule` property that stores original rule and `replace_index` property, that indicate which terminal were replace.
- `ContextFree.ChomskyTermRule`: It is class for rule, that directly rewrite nonterminal to terminal.

### Inverse operations

Eliminating of epsilon rules, removing of unit rules and transforming into Chomsky normal form have their inverse operations.
They are implemented on `InverseContextFree` class.

That functions needs just root nonterminal of parsed tree. They then traverse the parse tree and replace rules created by transformations by their original equivalent.

The operations needs to be perform in opposite order, that transformations occurs.

### Split rules

Because Grammar class split rules, which represents more than two rules,
there is need for algorithm, that replace splitted rule with the original one.
This algorithm is implemented on `InverseCommon` class as `splitted_rules` static method.

This call must be call as the last one. Also, you dont need to call this, if all of your rules have just single rule defined.

Algorithm is for now implemented only for Context-Free grammars.

In the following release of grammpy library, splitted rules should behave same as their original counterparts.
This method will than reflect it and may have empty implementation in the future.

## Helpers

Library provide from version 1.2.0 classes, that helps with parsed tree manipulation and traversing.

Class `Manipulation` can replace specific rule, nonterminal or terminal with different one.
The new element will be added into parsed tree and correctly connected to rest of the elements.

```python3
from grammpy_transforms import Manipulation
# ...
parsed = cyk(...)
Manipulation.replaceNode(parsed, MyNewNonterminal())
Manipulation.replaceRule(parsed.to_rule, MyNewRule())
# or use type deductions
Manipulation.replace(parsed, MyNewNonterminal())
Manipulation.replace(parsed.to_rule, MyNewRule())
```

Second class is `Traversing`. It contains static methods for post order and pre order traversing.
Methods traverse throught nonterminals, terminals and even the rules. If you want to traverse just nonterminals, use the `filter` buildin function.

```python3
from grammpy_transforms import Traversing
# ...
Traversing.postOrder(parsed)
Traversing.preOrder(parsed)
```

You can create your own traversing path by calling `traverse` static method.
Method accept root of the parsed tree and function accepting current traversing node and callback.
Passed method must call callback with every node you want to traverse.

```python3
from grammpy_transforms import Traversing
# ...
def post_order_traversing(elem, callback):
    if isinstance(elem, Nonterminal):
        for ch in elem.to_rule.to_symbols:
            yield callback(ch)
        yield ch

Traversing.traverse(parsed, post_order_traversing)
```

Alternatively, you can use `traverseSeparated` static method, that call different functions for nonterminals, terminals and rules.

```python3
def postOrder(root):
    def travRule(item, callback):
        resp = [callback(ch) for ch in item.to_symbols]
        return functools.reduce(operator.add, resp, []) + [item]
    def travNonterm(item, callback):
        return callback(item.to_rule) + [item]
    def travTerm(item, callback):
        return [item]
return Traversing.traverseSeparated(root, travRule, travNonterm, travTerm)
```

## Roadmap

Currently only small subset of operations are implemented.

Library should at least support these operations:
- Transform of grammar into valid LL(k) grammar
- Removing of recursion
- Transformations into another representation (like regular grammar to state machine), but this will be probably in separate package.

-----

Version: dev

Author: Patrik Valkovič

Licence: GNU General Public License v3.0
