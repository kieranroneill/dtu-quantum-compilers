from lark import Token, Tree
from libs import logging
from libs.errors import TypeCheckError
from utilities import symbol_of

from .exp_check import exp_check
from .symbols import BaseSymbol


def exp_unary_check(node: Tree, symbol_table: list[dict[str, BaseSymbol]]) -> None:
    """
    Type-checks an "exp_unary" node.

    Note: The grammar rules are stated in grammar_v1.lark, which is a subset of the grammar_v2.lark.

    Lark grammar: UNOP exp_unary

    Args:
        node (Tree): The "exp_unary" node to type-check.
        symbol_table (list[dict(str, BaseSymbol)]): A list of symbol tables, where each index is a scope level containing the symbols for that level. The symbol is a key/value pair (dict) where the key is the symbol name and the value is the symbol detail.

    Raises:
        TypeCheckError: If the "exp_unary" node fails the type check.
    """
    if not isinstance(node, Tree):
        logging.error("unexpected grammar form", node)

        raise TypeCheckError()

    operator_token = node.children[0]
    operator = str(operator_token.value)

    if not isinstance(operator_token, Token) or operator_token.type != "UNOP" or operator not in {"!", "not", "~", "-"}:
        logging.error(f'unexpected unary operator "{operator}"', operator_token)

        raise TypeCheckError()

    operand_token = node.children[1]
    symbol = symbol_of(operand_token)

    if symbol is None:
        logging.error(f'unsupported operand type "{str(operand_token.value)}"', operand_token)

        raise TypeCheckError()

    # bitwise negation must be "int"
    if operator == "~":
        if symbol.symbol is not "int":
            logging.error("bitwise negation requires integer operand", operand_token)

            raise TypeCheckError()

    # unary minus must be numeric (float or int)
    if operator == "-":
        if symbol.symbol != "int" or symbol.symbol != "float":
            logging.error("unary minus requires numeric operand", operand_token)

            raise TypeCheckError()

    return exp_check(operand_token, symbol_table)
