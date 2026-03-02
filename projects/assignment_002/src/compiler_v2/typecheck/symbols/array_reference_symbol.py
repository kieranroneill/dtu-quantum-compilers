from .base_symbol import BaseSymbol


class ArrayReferenceSymbol(BaseSymbol):
    """
    Represents an array symbol that uses a reference to another parameter ID for the size of the array, e.g., "x[a]".

    Attributes:
        _ref (str): The reference of the ID (the parameter name) indicating a reference to the size of the array, e.g., "x[a]" would give string "a".
    """

    def __init__(self, symbol: str, ref: str) -> None:
        super().__init__(symbol)

        self._ref = ref

    @property
    def ref(self) -> str:
        return self._ref
