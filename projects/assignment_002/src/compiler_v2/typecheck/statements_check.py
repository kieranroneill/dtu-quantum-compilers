from lark import Tree
from libs import logging
from libs.errors import TypeCheckError

from .statement_check import statement_check
from .symbols import BaseSymbol


def statements_check(node: Tree, symbol_table: list[dict[str, BaseSymbol]]) -> list[dict[str, BaseSymbol]]:
    if not isinstance(node, Tree) or str(node.data) != "statements":
        logging.error('expected "statements" node in block', node)

        raise TypeCheckError()

    _symbol_table = symbol_table.copy()

    for node in node.children:
        _symbol_table = statement_check(node, _symbol_table)

    return _symbol_table
