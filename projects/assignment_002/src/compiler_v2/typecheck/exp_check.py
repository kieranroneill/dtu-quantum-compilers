from lark import Tree
from libs import logging
from libs.errors import TypeCheckError

from .symbols import BaseSymbol


def exp_check(node: Tree, symbol_table: list[dict[str, BaseSymbol]]) -> list[dict[str, BaseSymbol]]:
    return symbol_table
