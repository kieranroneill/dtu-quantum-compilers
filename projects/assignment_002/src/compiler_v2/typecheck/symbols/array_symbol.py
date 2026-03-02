from .base_symbol import BaseSymbol


class ArraySymbol(BaseSymbol):
    """
    Represents an array symbol in the type system.

    Attributes:
        _size (int): The size of the array, e.g., "x[5]" would give integer 5.
    """

    def __init__(self, symbol: str, size: int) -> None:
        super().__init__(symbol)

        self._size = size

    @property
    def size(self) -> int:
        return self._size
