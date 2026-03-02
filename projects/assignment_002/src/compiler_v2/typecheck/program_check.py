from lark import Tree
from libs import logging
from libs.errors import CompileError, TypeCheckError

from .procedure_check import procedure_check
from .symbols import BaseSymbol


def program_check(ast: Tree, symbol_table: list[dict[str, BaseSymbol]]) -> list[dict[str, BaseSymbol]]:
    """
    Type-checks a CQ program.

    Args:
        ast (Tree): The parsed AST.
        symbol_table (list[dict(str, BaseSymbol)]): A list of symbol tables, where each index is a scope level containing the symbols for that level. The symbol is a key/value pair (dict) where the key is the symbol name and the value is the symbol detail.

    Returns:
        list[dict[str, BaseSymbol]]: A copy of the updated symbol table.

    Raises:
        CompileError: If the AST is not a Tree or if there are multiple procedures.
        TypeCheckError: If the "program" and its corresponding elements failed the type check.
    """
    if not isinstance(ast, Tree):
        logging.error(f'expected parse "Tree", but got "{type(ast)}"')

        raise CompileError()

    if str(ast.data) != "program":
        logging.error(f'expected start rule "program", got "{ast.data}"')

        raise TypeCheckError()

    procedures = ast.children

    if len(procedures) <= 0:
        return symbol_table

    if len(procedures) > 1:
        logging.error(f'expected one "procedure", got "{len(procedures)}" procedures')

        raise CompileError()

    procedure = procedures[0]

    return procedure_check(procedure, symbol_table)
