from lark import Token, Tree
from libs import logging
from libs.errors import TypeCheckError

from .symbols import BaseSymbol
from .utilities import symbol_of


def parameter_declarations_check(
    parameter_declarations_node: Tree, symbol_table: list[dict[str, BaseSymbol]]
) -> list[dict[str, BaseSymbol]]:
    """
    Type-check the parameters of a procedure.

    Lark grammar: TYPE ID | TYPE ID "[" (ID | INT) "]"

    Args:
        parameter_declarations_node (Tree): The parameters node to type-check.
        symbol_table (list[dict(str, BaseSymbol)]): A list of symbol tables, where each index is a scope level containing the symbols for that level. The symbol is a key/value pair (dict) where the key is the symbol name and the value is the symbol detail.

    Returns:
        list[dict[str, BaseSymbol]]: An updated symbol table with a copied entry for the current and nested scopes, all outer scopes remain unchanged with original references preserved.

    Raises:
        TypeCheckError: If the "parameter_declaration" failed the type check.
    """
    if (
        not isinstance(parameter_declarations_node, Tree)
        or str(parameter_declarations_node.data) != "parameter_declarations"
    ):
        logging.error('expected "parameter_declarations" node in procedure', parameter_declarations_node)

        raise TypeCheckError()

    _symbol_table = symbol_table.copy()  # shallow copy the scopes
    _symbol_table[-1] = symbol_table[-1].copy()  # copy the current scope so we don't mutate in place

    for parameter in parameter_declarations_node.children:
        if not isinstance(parameter, Tree) or str(parameter.data) != "parameter_declaration":
            logging.error('expected "parameter_declaration" node', parameter)

            raise TypeCheckError()

        children = parameter.children

        if len(children) > 3:
            logging.error(f'unexpected "parameter_declaration" shape', parameter)

            raise TypeCheckError()

        type_token = children[0]

        if not isinstance(type_token, Token) or type_token.type != "TYPE":
            logging.error('parameter type must be a "TYPE" token', type_token)

            raise TypeCheckError()

        name_token = children[1]

        if not isinstance(name_token, Token) or name_token.type != "ID":
            logging.error('parameter name must be an "ID" token', name_token)

            raise TypeCheckError()

        _type = str(type_token.value)
        name = str(name_token.value)

        if name in _symbol_table[-1]:
            logging.error(f'duplicate parameter name "{name}" in the same scope', name_token)

            raise TypeCheckError()

        symbol = symbol_of(parameter)

        if symbol is None:
            logging.error(f'unsupported parameter type "{_type}"', type_token)

            raise TypeCheckError()

        _symbol_table[-1][name] = symbol

    return _symbol_table
