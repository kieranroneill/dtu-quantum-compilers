from lark import Tree
from libs import logging
from libs.errors import TypeCheckError

from .declaration_check import declaration_check
from .symbols import BaseSymbol


def declarations_check(node: Tree, symbol_table: list[dict[str, BaseSymbol]]) -> list[dict[str, BaseSymbol]]:
    if not isinstance(node, Tree) or str(node.data) != "declarations":
        logging.error('expected "declarations" node in block', node)

        raise TypeCheckError()

    _symbol_table = symbol_table.copy()

    for node in node.children:
        _symbol_table = declaration_check(node, _symbol_table)

    return _symbol_table
