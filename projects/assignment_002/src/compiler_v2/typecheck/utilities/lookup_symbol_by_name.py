from ..symbols import BaseSymbol


def lookup_symbol_by_name(name: str, symbol_table: list[dict[str, BaseSymbol]]) -> BaseSymbol | None:
    """
    Gets the first symbol with the given name from the symbol table. As the symbol is in the form of a scope stack, it iterates backs through the stack returning the first symbol found with the given name.

    Args:
        name (str): The name of the symbol to lookup.
        symbol_table (list[dict(str, BaseSymbol)]): A list of symbol tables, where each index is a scope level containing the symbols for that level. The symbol is a key/value pair (dict) where the key is the symbol name and the value is the symbol detail.

    Returns:
        BaseSymbol | None: The symbol with the given name, or None if not found.
    """
    for scope in reversed(symbol_table):
        if name in scope:
            return scope[name]

    return None
