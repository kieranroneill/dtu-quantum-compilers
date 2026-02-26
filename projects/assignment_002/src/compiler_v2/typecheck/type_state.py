from dataclasses import dataclass


@dataclass(frozen=True)
class TypeState:
    """
    Holds scope stacks for declarations and types.

    symbol_table:  symbol table (declared names), used for scope/decl checks.
    tenv: type table (name -> CQ type string)
    """

    symbol_table: list[dict[str, object]]
    type_table: list[dict[str, str]]
