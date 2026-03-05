from lark import Token, Tree
from libs import logging
from libs.errors import TypeCheckError

from .exp_check import exp_check
from .symbols import BaseSymbol
from .utilities import symbol_of


def exp_binary_check(node: Tree, symbol_table: list[dict[str, BaseSymbol]]) -> None:
    """
    Type-checks an "exp_binary" node.

    Note: The grammar rules are stated in grammar_v1.lark, which is a subset of the grammar_v2.lark.

    Lark grammar: exp OP exp

    Args:
        node (Tree): The "exp_binary" node to type-check.
        symbol_table (list[dict(str, BaseSymbol)]): A list of symbol tables, where each index is a scope level containing the symbols for that level. The symbol is a key/value pair (dict) where the key is the symbol name and the value is the symbol detail.

    Raises:
        TypeCheckError: If the "exp_binary" node fails the type check.
    """
    if not isinstance(node, Tree):
        logging.error("unexpected grammar form", node)

        raise TypeCheckError()

    operator_token = node.children[1]

    if not isinstance(operator_token, Token) or operator_token.type not in {"PE", "MD", "AS", "CMP"}:
        logging.error("expected binary operator token in expression", operator_token)

        raise TypeCheckError()

    left_value_token = node.children[0]
    right_value_token = node.children[2]

    # check the left and right values
    exp_check(left_value_token, symbol_table)
    exp_check(right_value_token, symbol_table)

    operator_type = str(operator_token.type)
    operator_value = str(operator_token.value)
    left_value_symbol = symbol_of(left_value_token)
    right_value_symbol = symbol_of(right_value_token)

    # exponentiation base ** exponent
    if operator_type == "PE" and operator_value == "**":
        if left_value_symbol.symbol != "int" or left_value_token.symbol != "float":
            logging.error("exponentiation base must be numeric", node)

            raise TypeCheckError()

        if right_value_symbol.symbol != "int" or right_value_symbol.symbol != "float":
            logging.error("exponent must be numeric", node)

            raise TypeCheckError()

    return None
