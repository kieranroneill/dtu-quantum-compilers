from lark import Token, Tree
from libs import logging

from ..symbols import (
    ArrayReferenceSymbol,
    ArraySymbol,
    BaseSymbol,
    CBitSymbol,
    FloatSymbol,
    IntSymbol,
    QBitSymbol,
)


def symbol_of(item: Token | Tree) -> BaseSymbol | None:
    """
    Gets the symbol for the provided node/token.

    Args:
        item (Token | Tree): The node/token to parse the symbol for.

    Returns:
        (BaseSymbol | None): Returns the symbol for the provided node/token, or None if the symbol cannot be parsed.
    """
    _type = None

    if isinstance(item, Tree):
        _type = str(item.children[0].value)

        # if there is a third child, it is an array declaration, i.e. [TYPE, ID, -> (ID | INT)]
        if len(item.children) > 2:
            array_ref_token = item.children[2]

            if isinstance(array_ref_token, Token):
                if array_ref_token.type == "INT":
                    return ArraySymbol(_type, int(array_ref_token.value))

                if array_ref_token.type == "ID":
                    return ArrayReferenceSymbol(_type, str(array_ref_token.value))

                logging.warn('array reference must be an "ID" or "INT" token', item)

                return None

            logging.warn(f'unsupported type "{_type}"', item)

            return None

    if isinstance(item, Token):
        _type = str(item.value)

    if _type is not None:
        match _type:
            case "cbit":
                return CBitSymbol()
            case "float":
                return FloatSymbol()
            case "int":
                return IntSymbol()
            case "qbit":
                return QBitSymbol()
            case _:
                logging.warn(f'unsupported type "{_type}"', item)

                return None

    logging.warn(f"unable to parse symbol", item)

    return None
