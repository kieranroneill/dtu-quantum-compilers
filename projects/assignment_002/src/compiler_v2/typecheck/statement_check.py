from lark import Token, Tree
from libs import logging
from libs.errors import TypeCheckError

from .block_check import block_check
from .lval_check import lval_check
from .symbols import BaseSymbol
from .utilities import lookup_symbol_by_name


def statement_check(node: Tree, symbol_table: list[dict[str, BaseSymbol]]) -> list[dict[str, BaseSymbol]]:
    """
    Type-checks a "statement" node.

    Lark grammar: lval EQ exp ";"
        | qupdate ";"
        | qupdate IF lval ";"
        | procedure_call ";"
        | MEASURE lval "->" lval ";"
        | IF "(" exp ")" statement "else" statement
        | WHILE "(" exp ")" statement
        | block

    Args:
        node (Tree): The "statement" node to type-check.
        symbol_table (list[dict(str, BaseSymbol)]): A list of symbol tables, where each index is a scope level containing the symbols for that level. The symbol is a key/value pair (dict) where the key is the symbol name and the value is the symbol detail.

    Returns:
        list[dict[str, BaseSymbol]]: An updated symbol table with a copied entry for the current and nested scopes, all outer scopes remain unchanged with original references preserved.

    Raises:
        TypeCheckError: If the "statement" node fails the type check.
    """
    if not isinstance(node, Tree) or str(node.data) != "statement":
        logging.error('expected "statement" node', node)

        raise TypeCheckError()

    # grammar form:  lval EQ exp ";"
    if (
        len(node.children) == 3
        and isinstance(node.children[0], Tree)
        and str(node.children[0].data) == "lval"
        and isinstance(node.children[1], Token)
        and node.children[1].value == "="
        and isinstance(node.children[2], Tree)
        and str(node.children[2].data) == "exp"
    ):
        lval_node = node.children[0]

        lval_check(lval_node)

        name = lval_node.value
        symbol = lookup_symbol_by_name(lval_node.value)

        if symbol is None:
            logging.error(f'undefined variable "{name}"', lval_node)

            raise TypeCheckError()

        exp_node = node.children[2]

    # grammar: block
    if len(node.children) == 1 and isinstance(node.children[0], Tree) and str(node.children[0].data) == "block":
        return block_check(node.children[0], symbol_table)

    # TODO: implement other grammar forms for "statement" here

    logging.error("invalid declaration form", node)

    raise TypeCheckError()
