from lark import Token, Tree
from libs import logging
from libs.errors import TypeCheckError

from .parameter_declarations_check import parameter_declarations_check
from .statement_check import statement_check
from .symbols import BaseSymbol


def procedure_check(procedure: Tree, symbol_table: list[dict[str, BaseSymbol]]) -> list[dict[str, BaseSymbol]]:
    """
    Type-check a single procedure.

    Lark grammar: ID "(" parameter_declarations ")" statement

    Args:
        procedure (Tree): The procedure node to type-check.
        symbol_table (list[dict(str, BaseSymbol)]): A list of symbol tables, where each index is a scope level containing the symbols for that level. The symbol is a key/value pair (dict) where the key is the symbol name and the value is the symbol detail.

    Returns:
        list[dict[str, BaseSymbol]]: An updated symbol table with a copied entry for the current and nested scopes, all outer scopes remain unchanged with original references preserved.

    Raises:
        TypeCheckError: If the "procedure" fails the type check.
    """
    if not isinstance(procedure, Tree) or str(procedure.data) != "procedure":
        logging.error(f"expected \"procedure\" node, got {getattr(procedure, 'data', type(procedure))}", procedure)

        raise TypeCheckError()

    children = procedure.children

    if len(children) < 3:
        logging.error(f'invalid procedure shape, expected ["ID", "parameter_declarations", "statement"]', procedure)

        raise TypeCheckError()

    # <---------- "ID" check ---------->

    id_token = children[0]

    if not isinstance(id_token, Token) or id_token.type != "ID":
        logging.error(f'procedure name must be an "ID"', id_token)

        raise TypeCheckError()

    # <---------- "parameter_declarations" check ---------->

    _symbol_table = parameter_declarations_check(children[1], symbol_table)

    # <---------- "statement" check ---------->

    return statement_check(children[2], _symbol_table)
