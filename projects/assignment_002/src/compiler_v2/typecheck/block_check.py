from lark import Tree
from libs import logging
from libs.errors import TypeCheckError

from .declarations_check import declarations_check
from .statements_check import statements_check
from .symbols import BaseSymbol


def block_check(node: Tree, symbol_table: list[dict[str, BaseSymbol]]) -> list[dict[str, BaseSymbol]]:
    if not isinstance(node, Tree) or str(node.data) != "block":
        logging.error('expected "block" node', node)

        raise TypeCheckError()

    if len(node.children) != 2:
        logging.error(f"unexpected block shape", node)

        raise TypeCheckError()

    # add a new scope
    _symbol_table = symbol_table.copy().append({})

    _symbol_table = declarations_check(node.children[0], symbol_table)
    _symbol_table = statements_check(node.children[1], _symbol_table)

    # remove the scope
    _symbol_table.pop()

    return _symbol_table
