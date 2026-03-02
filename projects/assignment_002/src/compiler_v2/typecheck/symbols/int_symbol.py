from .base_symbol import BaseSymbol


class IntSymbol(BaseSymbol):
    def __init__(self) -> None:
        super().__init__("int")
