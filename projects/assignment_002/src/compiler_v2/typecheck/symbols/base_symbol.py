class BaseSymbol:
    """
    Base class for all symbols in the type system.

    Attributes:
        _symbol (str): The symbol, i.e., the type. E.g., "x = 1" would give the string "int".
    """

    def __init__(self, symbol: str) -> None:
        self._symbol = symbol

    def symbol(self) -> str:
        return self._symbol
