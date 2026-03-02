from .base_symbol import BaseSymbol


class QBitSymbol(BaseSymbol):
    def __init__(self) -> None:
        super().__init__("qbit")
