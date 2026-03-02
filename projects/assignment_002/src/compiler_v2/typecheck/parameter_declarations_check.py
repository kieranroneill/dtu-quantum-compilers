from lark import Token, Tree
from libs import logging
from libs.errors import TypeCheckError

from .symbols import (
    ArrayReferenceSymbol,
    ArraySymbol,
    BaseSymbol,
    CBitSymbol,
    FloatSymbol,
    IntSymbol,
    QBitSymbol,
)


def parameter_declarations_check(
    parameters: Tree, symbol_table: list[dict[str, BaseSymbol]]
) -> list[dict[str, BaseSymbol]]:
    """
    Type-check the parameters of a procedure.

    Lark grammar: TYPE ID | TYPE ID "[" (ID | INT) "]"

    Args:
        parameters (Tree): The parameters node to type-check.
        symbol_table (list[dict(str, BaseSymbol)]): A list of symbol tables, where each index is a scope level containing the symbols for that level. The symbol is a key/value pair (dict) where the key is the symbol name and the value is the symbol detail.

    Returns:
        list[dict[str, BaseSymbol]]: An updated symbol table with a copied entry for the current and nested scopes, all outer scopes remain unchanged with original references preserved.

    Raises:
        TypeCheckError: If the "parameter_declaration" failed the type check.
    """
    _symbol_table = symbol_table.copy()  # shallow copy the scopes
    _symbol_table[-1] = symbol_table[-1].copy()  # copy the current scope so we don't mutate in place

    for parameter in parameters.children:
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

        # if there is a third child, it is an array declaration, i.e. [TYPE, ID, -> (ID | INT)]
        if len(children) > 2:
            array_ref_token = children[2]

            if isinstance(array_ref_token, Token):
                if array_ref_token.type == "INT":
                    _symbol_table[-1][name] = ArraySymbol(_type, int(array_ref_token.value))

                    continue

                if array_ref_token.type == "ID":
                    _symbol_table[-1][name] = ArrayReferenceSymbol(_type, str(array_ref_token.value))

                    continue

            logging.error('array reference must be an "ID" or "INT" token', array_ref_token)

            raise TypeCheckError()

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
