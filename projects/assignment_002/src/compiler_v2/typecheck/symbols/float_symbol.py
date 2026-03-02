from .base_symbol import BaseSymbol


class FloatSymbol(BaseSymbol):
    def __init__(self) -> None:
        super().__init__("float")
