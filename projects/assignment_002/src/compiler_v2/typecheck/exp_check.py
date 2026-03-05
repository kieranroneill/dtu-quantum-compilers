from lark import Token, Tree
from libs import logging
from libs.errors import TypeCheckError

from .exp_binary_check import exp_binary_check
from .exp_unary_check import exp_unary_check
from .symbols import BaseSymbol
from .variable_check import variable_check


def exp_check(item: Token | Tree, symbol_table: list[dict[str, BaseSymbol]]) -> None:
    """
    Type-checks an "exp" node.

    Lark grammar:

    Args:
        item (Token | Tree): The "exp" node to type-check.
        symbol_table (list[dict(str, BaseSymbol)]): A list of symbol tables, where each index is a scope level containing the symbols for that level. The symbol is a key/value pair (dict) where the key is the symbol name and the value is the symbol detail.

    Raises:
        TypeCheckError: If the "exp" node fails the type check.
    """
    # grammar form: INT | FLOAT | NAMED_CONSTANT
    if isinstance(item, Token):
        if item.type in {"INT", "FLOAT", "NAMED_CONSTANT"}:
            return None

        logging.error(f'unexpected token "{item.type}"', item)

        raise TypeCheckError()

    # grammar form: variable
    if str(item.data) == "grammar_v1__variable":
        return variable_check(item, symbol_table)

    children = item.children

    match len(children):
        # grammar form: "(" exp ")"
        case 1:
            return exp_check(children[0], symbol_table)
        # grammar form: UNOP exp
        case 2:
            return exp_unary_check(item, symbol_table)
        # grammar form: exp BINOP exp
        case 3:
            return exp_binary_check(item, symbol_table)

    logging.error("invalid expression form", item)

    raise TypeCheckError()
