from lark import Token, Tree
from libs import logging
from libs.errors import TypeCheckError

from .exp_check import exp_check
from .symbols import BaseSymbol
from .utilities import lookup_symbol_by_name


def variable_check(node: Tree, symbol_table: list[dict[str, BaseSymbol]]) -> None:
    """
    Type-checks a "variable" node.

    Note: The grammar rules are stated in grammar_v1.lark, which is a subset of the grammar_v2.lark.

    Lark grammar: ID
        | ID "[" exp "]"

    Args:
        node (Tree): The "statement" node to type-check.
        symbol_table (list[dict(str, BaseSymbol)]): A list of symbol tables, where each index is a scope level containing the symbols for that level. The symbol is a key/value pair (dict) where the key is the symbol name and the value is the symbol detail.

    Raises:
        TypeCheckError: If the "variable" node fails the type check.
    """
    if not isinstance(node, Tree) or str(node.data) != "grammar_v1__variable":
        logging.error('expected "grammar_v1__variable" node', node)

        raise TypeCheckError()

    children = node.children

    # grammar form: ID
    if len(children) == 1 and isinstance(children[0], Token) and children[0].type == "ID":
        name = str(children[0].value)
        symbol = lookup_symbol_by_name(name, symbol_table)

        # if the symbol exists so we are successful
        if symbol is not None:
            return None

        logging.error(f'undefined variable "{name}"', node)

        raise TypeCheckError()

    # grammar form: ID "[" exp "]"
    if (
        len(children) == 2
        and isinstance(children[0], Token)
        and children[0].type == "ID"
        and isinstance(children[1], Tree)
    ):
        name = str(children[0].value)

        # check the symbol exists
        symbol = lookup_symbol_by_name(name, symbol_table)

        if symbol is None:
            logging.error(f'undefined variable "{name}"', node)

            raise TypeCheckError()

        return exp_check(children[1], symbol_table)

    logging.error("invalid variable form", node)

    raise TypeCheckError()
