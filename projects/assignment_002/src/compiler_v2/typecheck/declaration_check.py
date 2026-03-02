from lark import Token, Tree
from libs import logging
from libs.errors import TypeCheckError

from .lval_check import lval_check
from .symbols import (
    BaseSymbol,
    CBitSymbol,
    FloatSymbol,
    IntSymbol,
    QBitSymbol,
)


def declaration_check(node: Tree, symbol_table: list[dict[str, BaseSymbol]]) -> list[dict[str, BaseSymbol]]:
    """
    Type-checks the "declaration" node.

    Lark grammar: TYPE lval ";"
        | TYPE ID "=" exp ";"
        | TYPE ID "[" INT "]" "=" "{" exps "}" ";"

    Args:
        node (Tree): The "declaration" node to type-check.
        symbol_table (list[dict(str, BaseSymbol)]): A list of symbol tables, where each index is a scope level containing the symbols for that level. The symbol is a key/value pair (dict) where the key is the symbol name and the value is the symbol detail.

    Returns:
        list[dict[str, BaseSymbol]]: An updated symbol table with a copied entry for the current and nested scopes, all outer scopes remain unchanged with original references preserved.

    Raises:
        TypeCheckError: If the "declaration" node fails the type check.
    """
    if not isinstance(node, Tree) or str(node.data) != "declaration":
        logging.error('expected "declaration" node', node)

        raise TypeCheckError()

    _symbol_table = symbol_table.copy()
    _symbol_table[-1] = symbol_table[-1].copy()

    # grammar: TYPE lval ";"
    if len(node.children) >= 2 and isinstance(node.children[0], Token) and node.children[0].type == "TYPE":
        lval_node = node.children[1]

        lval_check(lval_node)

        name = str(lval_node.value)

        if name in _symbol_table[-1]:
            logging.error(f'duplicate declaration name "{name}" in the same scope', lval_node)

            raise TypeCheckError()

        type_token = node.children[0]
        _type = str(type_token.value)

        match _type:
            case "cbit":
                _symbol_table[-1][name] = CBitSymbol()
            case "float":
                _symbol_table[-1][name] = FloatSymbol()
            case "int":
                _symbol_table[-1][name] = IntSymbol()
            case "qbit":
                _symbol_table[-1][name] = QBitSymbol()
            case _:
                logging.error(f'unsupported parameter type "{_type}"', type_token)

                raise TypeCheckError()

        return _symbol_table

    # TODO: implement other grammar forms for declaration here

    logging.error("invalid declaration form", node)

    raise TypeCheckError()
